import { sharedSecret } from './crypto.js';

export const runExchange = (sender, receiver, params) => {
  const sharedSender = sharedSecret(receiver.publicKey, sender.secret, params.P);
  const sharedReceiver = sharedSecret(sender.publicKey, receiver.secret, params.P);

  const steps = [
    `<strong>Общие параметры</strong>: P=${params.P}, G=${params.G}`,
    `<strong>${sender.name}</strong> вычисляет открытый ключ: ${params.G}^${sender.secret} mod ${params.P} = ${sender.publicKey}`,
    `<strong>${receiver.name}</strong> вычисляет открытый ключ: ${params.G}^${receiver.secret} mod ${params.P} = ${receiver.publicKey}`,
    `<strong>${sender.name}</strong> получает ${receiver.publicKey} и выводит общий ключ: ${receiver.publicKey}^${sender.secret} mod ${params.P} = ${sharedSender}`,
    `<strong>${receiver.name}</strong> получает ${sender.publicKey} и выводит общий ключ: ${sender.publicKey}^${receiver.secret} mod ${params.P} = ${sharedReceiver}`
  ];

  return {
    steps,
    sharedSender,
    sharedReceiver,
    match: sharedSender === sharedReceiver,
    shared: sharedSender,
    details: {
      params,
      sender,
      receiver,
      calculations: {
        senderPublic: `${params.G}^${sender.secret} mod ${params.P} = ${sender.publicKey}`,
        receiverPublic: `${params.G}^${receiver.secret} mod ${params.P} = ${receiver.publicKey}`,
        senderShared: `${receiver.publicKey}^${sender.secret} mod ${params.P} = ${sharedSender}`,
        receiverShared: `${sender.publicKey}^${receiver.secret} mod ${params.P} = ${sharedReceiver}`
      }
    }
  };
};
