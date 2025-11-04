
# Criar arquivo adicional com exemplo de integração WebSocket avançada do Eleven Labs

elevenlabs_ws_example = """// ============================================
// EXEMPLO AVANÇADO: Eleven Labs WebSocket
// Streaming de input em tempo real
// ============================================

const WebSocket = require('ws');
const { Readable } = require('stream');

class ElevenLabsWebSocketClient {
  constructor(voiceId, apiKey, modelId = 'eleven_turbo_v2_5') {
    this.voiceId = voiceId;
    this.apiKey = apiKey;
    this.modelId = modelId;
    this.ws = null;
    this.isConnected = false;
    this.audioChunks = [];
  }

  // Conectar ao WebSocket do Eleven Labs
  connect() {
    return new Promise((resolve, reject) => {
      const wsUrl = `wss://api.elevenlabs.io/v1/text-to-speech/${this.voiceId}/stream-input?model_id=${this.modelId}`;
      
      this.ws = new WebSocket(wsUrl);
      
      this.ws.on('open', () => {
        console.log('✅ Conectado ao Eleven Labs WebSocket');
        
        // Enviar configuração inicial
        const initMessage = {
          text: ' ',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            style: 0.5,
            use_speaker_boost: true
          },
          xi_api_key: this.apiKey
        };
        
        this.ws.send(JSON.stringify(initMessage));
        this.isConnected = true;
        resolve();
      });
      
      this.ws.on('message', (data) => {
        try {
          const response = JSON.parse(data.toString());
          
          if (response.audio) {
            // Converter base64 para buffer
            const audioBuffer = Buffer.from(response.audio, 'base64');
            this.audioChunks.push(audioBuffer);
            
            // Emitir evento de novo chunk de áudio
            this.emit('audioChunk', audioBuffer);
          }
          
          if (response.isFinal) {
            console.log('🎵 Geração de áudio finalizada');
            this.emit('audioComplete', Buffer.concat(this.audioChunks));
            this.audioChunks = [];
          }
          
          if (response.alignment) {
            // Informações de alinhamento de texto-áudio
            this.emit('alignment', response.alignment);
          }
          
        } catch (error) {
          console.error('❌ Erro ao processar mensagem:', error);
        }
      });
      
      this.ws.on('error', (error) => {
        console.error('❌ WebSocket erro:', error);
        reject(error);
      });
      
      this.ws.on('close', () => {
        console.log('👋 Conexão fechada');
        this.isConnected = false;
        this.emit('close');
      });
    });
  }

  // Enviar texto para conversão (streaming)
  sendText(text, tryTriggerGeneration = true) {
    if (!this.isConnected) {
      throw new Error('WebSocket não conectado');
    }
    
    const message = {
      text: text + ' ',  // Adicionar espaço no final
      try_trigger_generation: tryTriggerGeneration
    };
    
    this.ws.send(JSON.stringify(message));
  }

  // Finalizar stream
  finalize() {
    if (!this.isConnected) {
      return;
    }
    
    const endMessage = {
      text: ''
    };
    
    this.ws.send(JSON.stringify(endMessage));
  }

  // Fechar conexão
  close() {
    if (this.ws) {
      this.ws.close();
    }
  }

  // Sistema de eventos simples
  events = {};
  
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  }
  
  emit(event, data) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
  }
}

// ============================================
// EXEMPLO DE USO
// ============================================

async function exemploDeUso() {
  const voiceId = '21m00Tcm4TlvDq8ikWAM'; // Rachel voice
  const apiKey = process.env.ELEVENLABS_API_KEY;
  
  const elevenLabs = new ElevenLabsWebSocketClient(voiceId, apiKey);
  
  // Configurar listeners
  elevenLabs.on('audioChunk', (chunk) => {
    console.log(`📦 Recebido chunk de ${chunk.length} bytes`);
    // Aqui você pode processar ou enviar para o cliente
  });
  
  elevenLabs.on('audioComplete', (fullAudio) => {
    console.log(`✅ Áudio completo: ${fullAudio.length} bytes`);
    // Salvar ou enviar áudio completo
  });
  
  elevenLabs.on('close', () => {
    console.log('Conexão encerrada');
  });
  
  try {
    // Conectar
    await elevenLabs.connect();
    
    // Enviar texto em chunks (simulando streaming)
    elevenLabs.sendText('Olá! ');
    elevenLabs.sendText('Como posso ajudar você hoje? ');
    elevenLabs.sendText('Estou aqui para responder suas perguntas. ');
    
    // Finalizar
    elevenLabs.finalize();
    
    // Aguardar processamento
    setTimeout(() => {
      elevenLabs.close();
    }, 5000);
    
  } catch (error) {
    console.error('Erro:', error);
  }
}

// ============================================
// INTEGRAÇÃO COM SERVIDOR EXPRESS + WEBSOCKET
// ============================================

function setupElevenLabsWebSocketRoute(wss) {
  wss.on('connection', async (ws) => {
    let elevenLabsClient = null;
    
    ws.on('message', async (data) => {
      try {
        const message = JSON.parse(data.toString());
        
        if (message.type === 'startTTS') {
          // Iniciar conexão com Eleven Labs
          elevenLabsClient = new ElevenLabsWebSocketClient(
            message.voiceId || '21m00Tcm4TlvDq8ikWAM',
            process.env.ELEVENLABS_API_KEY
          );
          
          // Redirecionar chunks de áudio para o cliente WebSocket
          elevenLabsClient.on('audioChunk', (chunk) => {
            ws.send(JSON.stringify({
              type: 'audioChunk',
              audio: chunk.toString('base64')
            }));
          });
          
          elevenLabsClient.on('audioComplete', (fullAudio) => {
            ws.send(JSON.stringify({
              type: 'audioComplete',
              size: fullAudio.length
            }));
          });
          
          await elevenLabsClient.connect();
        }
        
        if (message.type === 'sendText' && elevenLabsClient) {
          elevenLabsClient.sendText(message.text);
        }
        
        if (message.type === 'finalizeTTS' && elevenLabsClient) {
          elevenLabsClient.finalize();
        }
        
      } catch (error) {
        console.error('Erro:', error);
        ws.send(JSON.stringify({
          type: 'error',
          message: error.message
        }));
      }
    });
    
    ws.on('close', () => {
      if (elevenLabsClient) {
        elevenLabsClient.close();
      }
    });
  });
}

module.exports = {
  ElevenLabsWebSocketClient,
  setupElevenLabsWebSocketRoute
};
"""

# Salvar arquivo
with open('elevenlabs_websocket_advanced.js', 'w', encoding='utf-8') as f:
    f.write(elevenlabs_ws_example)

print("✅ Arquivo elevenlabs_websocket_advanced.js criado!")
print("\n" + "="*60)
