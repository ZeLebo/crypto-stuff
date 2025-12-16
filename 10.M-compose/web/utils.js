// Utility helpers shared across the web app
export const mod = (n, m) => ((n % m) + m) % m;

export function isPrime(n) {
  if (n < 2) return false;
  for (let i = 2; i * i <= n; i += 1) {
    if (n % i === 0) return false;
  }
  return true;
}

function extendedGcd(a, b) {
  if (a === 0) return { gcd: b, x: 0, y: 1 };
  const { gcd, x: x1, y: y1 } = extendedGcd(b % a, a);
  return { gcd, x: y1 - Math.floor(b / a) * x1, y: x1 };
}

export function modInverse(a, m) {
  const { gcd, x } = extendedGcd(mod(a, m), m);
  if (gcd !== 1) throw new Error(`mod_inverse(${a}, ${m}) is not defined`);
  return mod(x, m);
}
