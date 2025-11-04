const express = require('express');
const cors = require('cors');
const http = require('http');
const { WebSocketServer } = require('ws');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const WebSocket = require('ws');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Inicializar Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });

// Criar servidor HTTP
const server = http.createServer(app);

// Criar servidor WebSocket
const wss = new WebSocketServer({ server });

// Gerenciar conexões WebSocket
const clients = new Map();

wss.on('connection', (ws) => {
  const clientId = Date.now().toString();
  clients.set(clientId, ws);

  console.log(`✅ Novo cliente conectado: ${clientId}`);

  // Enviar ID do cliente
  ws.send(JSON.stringify({ 
    type: 'connected', 
    clientId,
    message: 'Conectado ao servidor de IA com sucesso!' 
  }));

  // Receber mensagens do cliente
  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data.toString());

      if (message.type === 'chat') {
        console.log(`💬 Mensagem recebida de ${clientId}: ${message.text}`);

        // Processar com Gemini
        const result = await model.generateContent(message.text);
        const response = await result.response;
        const text = response.text();

        // Enviar resposta de volta
        ws.send(JSON.stringify({
          type: 'chatResponse',
          text: text,
          timestamp: new Date().toISOString()
        }));

        // Notificar outros clientes (broadcast)
        broadcastMessage({
          type: 'userActivity',
          clientId,
          activity: 'enviou uma mensagem'
        }, clientId);
      }

      if (message.type === 'audioRequest') {
        // Sinalizar que áudio está sendo gerado
        ws.send(JSON.stringify({
          type: 'audioProcessing',
          status: 'generating'
        }));
      }

    } catch (error) {
      console.error('❌ Erro ao processar mensagem:', error);
      ws.send(JSON.stringify({ 
        type: 'error', 
        message: 'Erro ao processar mensagem' 
      }));
    }
  });

  ws.on('close', () => {
    console.log(`👋 Cliente desconectado: ${clientId}`);
    clients.delete(clientId);
  });

  ws.on('error', (error) => {
    console.error(`❌ Erro no WebSocket ${clientId}:`, error);
  });
});

// Função para broadcast de mensagens
function broadcastMessage(message, excludeClientId = null) {
  clients.forEach((client, id) => {
    if (id !== excludeClientId && client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message));
    }
  });
}

// Endpoint para Eleven Labs TTS
app.post('/api/tts', async (req, res) => {
  try {
    const { text, voiceId = '21m00Tcm4TlvDq8ikWAM' } = req.body;

    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        method: 'POST',
        headers: {
          'Accept': 'audio/mpeg',
          'Content-Type': 'application/json',
          'xi-api-key': process.env.ELEVENLABS_API_KEY
        },
        body: JSON.stringify({
          text,
          model_id: 'eleven_turbo_v2_5',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
            style: 0.5,
            use_speaker_boost: true
          }
        })
      }
    );

    if (!response.ok) {
      throw new Error(`Eleven Labs API erro: ${response.statusText}`);
    }

    const audioBuffer = await response.arrayBuffer();

    res.set({
      'Content-Type': 'audio/mpeg',
      'Content-Length': audioBuffer.byteLength
    });
    res.send(Buffer.from(audioBuffer));

  } catch (error) {
    console.error('❌ Erro no TTS:', error);
    res.status(500).json({ error: 'Erro ao gerar áudio' });
  }
});

// Endpoint para streaming TTS com Eleven Labs (WebSocket)
app.post('/api/tts-stream', async (req, res) => {
  try {
    const { text, voiceId = '21m00Tcm4TlvDq8ikWAM' } = req.body;

    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream`,
      {
        method: 'POST',
        headers: {
          'Accept': 'audio/mpeg',
          'Content-Type': 'application/json',
          'xi-api-key': process.env.ELEVENLABS_API_KEY
        },
        body: JSON.stringify({
          text,
          model_id: 'eleven_turbo_v2_5',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75
          },
          optimize_streaming_latency: 3
        })
      }
    );

    if (!response.ok) {
      throw new Error(`Eleven Labs API erro: ${response.statusText}`);
    }

    res.set({
      'Content-Type': 'audio/mpeg',
      'Transfer-Encoding': 'chunked'
    });

    // Stream de áudio
    response.body.pipe(res);

  } catch (error) {
    console.error('❌ Erro no TTS streaming:', error);
    res.status(500).json({ error: 'Erro ao gerar áudio' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    clients: clients.size,
    timestamp: new Date().toISOString()
  });
});

server.listen(PORT, () => {
  console.log(`🚀 Servidor rodando na porta ${PORT}`);
  console.log(`🔌 WebSocket disponível em ws://localhost:${PORT}`);
  console.log(`🌐 HTTP disponível em http://localhost:${PORT}`);
});
