# 🤖 Assistente de Voz IA - Real Time

Assistente de voz inteligente com integração avançada de **Gemini AI**, **Eleven Labs TTS** e **WebSocket** para comunicação em tempo real.

## ⚡ Deploy Rápido

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/seujao436/tts-testeDnovo)

> **⚠️ Importante**: Durante o deploy, você precisará configurar as variáveis de ambiente:
> - `GEMINI_API_KEY` - Sua chave da API do Gemini
> - `ELEVENLABS_API_KEY` - Sua chave da API do Eleven Labs
> - `PORT` - Porta do servidor (padrão: 3000)

## 🚀 Funcionalidades

- ✅ **WebSocket em tempo real** para comunicação bidirecional
- 🎤 **Reconhecimento de voz** usando Web Speech API
- 🔊 **Text-to-Speech** com Eleven Labs (voz ultra-realista)
- 🤖 **Processamento de IA** com Gemini 2.0 Flash
- 🎨 **Interface moderna** e responsiva
- 📊 **Visualizador de áudio** em tempo real
- 🔔 **Notificações** de atividade entre clientes
- 💾 **Sistema de broadcast** para múltiplos clientes

## 📋 Pré-requisitos

- Node.js 18+
- Conta no Google AI (Gemini API)
- Conta no Eleven Labs
- Navegador moderno (Chrome, Firefox, Edge)

## 🔧 Instalação

### 1. Clone ou crie o projeto

```bash
mkdir assistente-voz-ia
cd assistente-voz-ia
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
ELEVENLABS_API_KEY=sua_chave_elevenlabs_aqui
PORT=3000
```

#### Como obter as chaves:

**Gemini API Key:**
1. Acesse: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave API
3. Copie e cole no .env

**Eleven Labs API Key:**
1. Acesse: [https://elevenlabs.io](https://elevenlabs.io)
2. Vá em Profile → API Keys
3. Gere uma nova chave
4. Copie e cole no .env

### 4. Estrutura de arquivos

```
assistente-voz-ia/
├── server.js              # Servidor principal com WebSocket
├── package.json           # Dependências
├── .env                   # Variáveis de ambiente (NÃO commitar!)
├── .gitignore            # Arquivos a ignorar
└── public/
    └── index.html        # Interface do usuário
```

### 5. Execute o servidor

```bash
# Modo desenvolvimento (com auto-reload)
npm run dev

# Modo produção
npm start
```

Acesse: `http://localhost:3000`

## 🎯 Como Usar

1. **Conectar**: Clique em "🔌 Conectar" para estabelecer conexão WebSocket
2. **Falar**: Clique em "🎤 Falar" e fale sua pergunta
3. **Ouvir**: O assistente processará e responderá com voz

## 🌐 Deploy no Render.com

### 1. Prepare o repositório

```bash
git init
git add .
git commit -m "Assistente de voz IA com WebSocket"
git remote add origin seu-repositorio.git
git push -u origin main
```

### 2. Configure o Render

1. Acesse [https://render.com](https://render.com)
2. Crie um novo **Web Service**
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Environment Variables**: Adicione suas API keys

### 3. Variáveis de ambiente no Render

```
GEMINI_API_KEY=sua_chave_gemini
ELEVENLABS_API_KEY=sua_chave_elevenlabs
PORT=3000
```

## 🔒 Segurança

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` no Git!

Adicione ao `.gitignore`:
```
node_modules/
.env
*.log
```

## 📡 API Endpoints

### WebSocket
- **URL**: `ws://localhost:3000`
- **Mensagens suportadas**:
  - `{ type: 'chat', text: 'sua mensagem' }` - Enviar mensagem
  - `{ type: 'audioRequest' }` - Solicitar áudio

### HTTP Endpoints

#### POST `/api/tts`
Gera áudio a partir de texto (não-streaming)

**Request:**
```json
{
  "text": "Olá, como posso ajudar?",
  "voiceId": "21m00Tcm4TlvDq8ikWAM"
}
```

**Response:** `audio/mpeg`

#### POST `/api/tts-stream`
Gera áudio com streaming (baixa latência)

**Request:**
```json
{
  "text": "Texto para converter",
  "voiceId": "21m00Tcm4TlvDq8ikWAM"
}
```

**Response:** `audio/mpeg` (streaming)

#### GET `/health`
Verifica status do servidor

**Response:**
```json
{
  "status": "ok",
  "clients": 2,
  "timestamp": "2025-11-04T20:00:00.000Z"
}
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Node.js + Express
- **WebSocket**: ws (biblioteca)
- **IA**: Google Gemini 2.0 Flash
- **TTS**: Eleven Labs API
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Speech Recognition**: Web Speech API

## 🎨 Recursos Avançados

### WebSocket Features
- ✅ Conexões persistentes
- ✅ Comunicação bidirecional
- ✅ Broadcast para múltiplos clientes
- ✅ Gerenciamento de conexões
- ✅ Reconexão automática (client-side)

### Eleven Labs Integration
- ✅ TTS de alta qualidade
- ✅ Streaming de áudio (baixa latência)
- ✅ Múltiplas vozes disponíveis
- ✅ Configurações de voz personalizáveis

### Gemini AI
- ✅ Modelo Gemini 2.0 Flash
- ✅ Respostas contextualizadas
- ✅ Processamento rápido

## 📝 Customização

### Trocar a voz do Eleven Labs

Acesse: [https://elevenlabs.io/voice-library](https://elevenlabs.io/voice-library)

```javascript
// No server.js, altere:
const voiceId = 'SEU_VOICE_ID_AQUI';
```

### Personalizar instruções do Gemini

```javascript
const systemInstruction = `
  Você é um assistente prestativo que...
  [suas instruções aqui]
`;
```

## 🐛 Troubleshooting

### Erro: "WebSocket connection failed"
- Verifique se o servidor está rodando
- Confirme a porta correta (padrão: 3000)

### Erro: "Reconhecimento de voz não suportado"
- Use navegadores Chromium (Chrome, Edge, Brave)
- Verifique permissões de microfone

### Erro: "Eleven Labs API error"
- Verifique sua API key
- Confirme créditos disponíveis em sua conta

### Erro: "Gemini API error"
- Verifique sua API key do Google
- Confirme que a API está ativada

## 📚 Documentação

- [Gemini API](https://ai.google.dev/gemini-api/docs)
- [Eleven Labs Docs](https://elevenlabs.io/docs)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fork o projeto
2. Criar uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📄 Licença

MIT License - veja LICENSE para mais detalhes

## ✨ Autor

Desenvolvido com ❤️ para a comunidade

---

**Dica Pro**: Use o plano gratuito do Eleven Labs para testes (10k caracteres/mês)
