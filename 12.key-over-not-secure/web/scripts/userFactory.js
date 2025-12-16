import { randomSecret, makePublicKey } from './crypto.js';

const palette = [
  '#ff6f4d',
  '#45f0c3',
  '#55a8ff',
  '#fbb040',
  '#b86bff',
  '#6be7ff',
  '#ff9fb6',
  '#7ef29c'
];

export const buildUsers = (count, params) => {
  return Array.from({ length: count }).map((_, idx) => {
    const name = `A${idx + 1}`;
    const secret = randomSecret(params.P);
    const publicKey = makePublicKey(params.G, secret, params.P);
    return {
      id: idx,
      name,
      secret,
      publicKey,
      color: palette[idx % palette.length]
    };
  });
};

export const buildAttacker = (params, label = 'Mallory') => {
  const secret = randomSecret(params.P);
  const publicKey = makePublicKey(params.G, secret, params.P);
  return { name: label, secret, publicKey, color: '#ff3c7d' };
};
