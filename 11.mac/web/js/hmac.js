import { concatBytes, constantTimeEqual } from "./utils.js";

const BLOCK_LEN = 64; // block size for SHA-256
const IPAD = 0x36;
const OPAD = 0x5c;

// SHA-256 using WebCrypto. Returns Uint8Array.
async function sha256(bytes) {
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return new Uint8Array(digest);
}

// Manual HMAC construction:
// 1) Подгоняем ключ под размер блока (хешируем или дополняем нулями).
// 2) XOR с ipad/opad, считаем вложенные SHA256.
export async function hmacSha256(keyBytes, messageBytes) {
  let k = keyBytes;
  if (k.length > BLOCK_LEN) {
    k = await sha256(k);
  }
  if (k.length < BLOCK_LEN) {
    const padded = new Uint8Array(BLOCK_LEN);
    padded.set(k);
    k = padded;
  }

  const ipad = new Uint8Array(BLOCK_LEN).fill(IPAD);
  const opad = new Uint8Array(BLOCK_LEN).fill(OPAD);

  const kIpad = k.map((b, i) => b ^ ipad[i]);
  const kOpad = k.map((b, i) => b ^ opad[i]);

  const inner = await sha256(concatBytes(kIpad, messageBytes));
  const outer = await sha256(concatBytes(kOpad, inner));
  return outer;
}

export function verifyMac(keyBytes, messageBytes, receivedMac) {
  return hmacSha256(keyBytes, messageBytes).then((calc) =>
    constantTimeEqual(calc, receivedMac)
  );
}
