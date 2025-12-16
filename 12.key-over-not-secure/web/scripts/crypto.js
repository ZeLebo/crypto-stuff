const PRIMES = [307, 311, 313, 317, 331, 337, 379, 383, 389, 397];

const randomItem = (items) => items[Math.floor(Math.random() * items.length)];

export const generatePublicParams = () => {
  const P = randomItem(PRIMES);
  const G = 2 + Math.floor(Math.random() * (P - 3));
  return { P, G };
};

export const randomSecret = (p) => 2 + Math.floor(Math.random() * (p - 3));

export const modExp = (base, exponent, modulus) => {
  let result = 1n;
  let b = BigInt(base);
  let e = BigInt(exponent);
  const m = BigInt(modulus);

  while (e > 0n) {
    if (e & 1n) {
      result = (result * b) % m;
    }
    e >>= 1n;
    b = (b * b) % m;
  }
  return Number(result);
};

export const makePublicKey = (G, secret, P) => modExp(G, secret, P);

export const sharedSecret = (publicKey, secret, P) => modExp(publicKey, secret, P);
