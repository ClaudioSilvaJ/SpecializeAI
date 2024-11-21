const { useMultiFileAuthState, default: makeWASocket, DisconnectReason } = require("@whiskeysockets/baileys");
const axios = require('axios');

const lastMessageTimestamps = new Map();
const messageBuffers = new Map();
const messageTimers = new Map();

async function connectWhats() {
  const { state, saveCreds } = await useMultiFileAuthState('./auth_info.json');

  const sock = makeWASocket({
    printQRInTerminal: true,
    auth: state,
  });

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect } = update;
    if (connection === 'close') {
      const error = (lastDisconnect?.error)?.output?.statusCode;
      console.log(`Connection closed due to error: ${error}`);
      const shouldReconnect = error != DisconnectReason.loggedOut;
      if (shouldReconnect) {
        console.log('Reconnecting...');
        setTimeout(() => connectWhats(), 5000);
      }
    } else if (connection === 'open') {
      console.log('Connection was opened');
    }
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('messages.upsert', async m => {
    if (m.messages[0].key.fromMe) return;
    const message = m.messages[0];
    const remoteJid = message.key.remoteJid;
    const userMessage = message.message.conversation;
    const now = Date.now();
    const lastTimestamp = lastMessageTimestamps.get(remoteJid) || 0;

    if (now - lastTimestamp > 600000) {
      lastMessageTimestamps.set(remoteJid, now);
      await sock.sendMessage(remoteJid, { text: 'Olá! Este bot está em fase experimental. Siga as instruções abaixo: Descreva seus sintomas em sequência. Não é necessário enviar mensagens separadas; você pode enviar tudo em uma única mensagem. Também não é preciso usar linguagem técnica ou formal.' });
      return;
    }
    if (!messageBuffers.has(remoteJid)) {
      messageBuffers.set(remoteJid, []);
    }
    messageBuffers.get(remoteJid).push(userMessage);

    if (messageTimers.has(remoteJid)) {
      clearTimeout(messageTimers.get(remoteJid));
    }

    messageTimers.set(remoteJid, setTimeout(async () => {
      const messages = messageBuffers.get(remoteJid).join(' ');
      messageBuffers.delete(remoteJid);
      messageTimers.delete(remoteJid);

      if (messages.length < 10) {
        await sock.sendMessage(remoteJid, { text: `Sua mensagem é muito curta! Seja mais específico` });
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:8000/extract-symptoms', { message: messages });
        const sintomas = response.data.sintomas;
        const especialidade = response.data.especialidade;
        
        if (sintomas[0] === 'Nenhum') {
          await sock.sendMessage(remoteJid, { text: `Infelizmente não consegui obter nenhum sintoma de sua mensagem, pode tentar novamente?` });
          return;
        }

        if (!especialidade) {
          await sock.sendMessage(remoteJid, { text: `Seus sintomas: ${sintomas} \nConsulte com um médico geral` });
        } else {
          await sock.sendMessage(remoteJid, { text: `Seus sintomas: ${sintomas} \nConsulte com um: ${especialidade}` });
        }
      } catch (error) {
        console.error("Erro ao chamar a API:", error);
        await sock.sendMessage(remoteJid, { text: "Houve um erro ao processar sua mensagem." });
      }
    }, 5000)); // Define espera de 5 segundos para concatenar mensagens antes de enviar à API
  });
}

connectWhats();
