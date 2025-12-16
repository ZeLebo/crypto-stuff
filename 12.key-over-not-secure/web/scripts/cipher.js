const deriveByte = (key) => (key % 251) + 5;

const toHex = (bytes) => Array.from(bytes).map((b) => b.toString(16).padStart(2, '0')).join('');
const fromHex = (hex) => {
  const bytes = [];
  for (let i = 0; i < hex.length; i += 2) {
    bytes.push(parseInt(hex.slice(i, i + 2), 16));
  }
  return bytes;
};

export const encryptMessage = (text, key) => {
  const shift = deriveByte(key);
  const encoded = new TextEncoder().encode(text);
  const cipherBytes = encoded.map((byte, idx) => byte ^ ((shift + idx * 7) % 256));
  return toHex(cipherBytes);
};

export const decryptMessage = (hex, key) => {
  const shift = deriveByte(key);
  const bytes = fromHex(hex);
  const plainBytes = bytes.map((byte, idx) => byte ^ ((shift + idx * 7) % 256));
  return new TextDecoder('utf-8', { fatal: false }).decode(new Uint8Array(plainBytes));
};
