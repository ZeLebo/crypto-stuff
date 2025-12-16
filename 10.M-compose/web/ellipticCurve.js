import { mod, modInverse } from "./utils.js";

export const infinityPoint = { isInfinity: true };

export function isOnCurve(point, A, B, P) {
  if (point.isInfinity) return true;
  return mod(point.y * point.y, P) === mod(point.x ** 3 + A * point.x + B, P);
}

export function addPoints(P1, P2, curve) {
  const { A, P } = curve;
  // Identity rules
  if (P1.isInfinity) return P2;
  if (P2.isInfinity) return P1;

  // P + (-P) = O
  if (P1.x === P2.x && mod(P1.y + P2.y, P) === 0) return infinityPoint;

  // Tangent (doubling) vs secant slopes
  let slope;
  if (P1.x === P2.x && P1.y === P2.y) {
    if (P1.y === 0) return infinityPoint;
    const numerator = mod(3 * P1.x * P1.x + A, P);
    const denominator = mod(2 * P1.y, P);
    slope = mod(numerator * modInverse(denominator, P), P);
  } else {
    const numerator = mod(P2.y - P1.y, P);
    const denominator = mod(P2.x - P1.x, P);
    if (denominator === 0) return infinityPoint;
    slope = mod(numerator * modInverse(denominator, P), P);
  }

  const x3 = mod(slope * slope - P1.x - P2.x, P);
  const y3 = mod(slope * (P1.x - x3) - P1.y, P);
  return { x: x3, y: y3, isInfinity: false };
}

export function scalarMultiply(k, point, curve) {
  if (k === 0 || point.isInfinity) return infinityPoint;
  let n = k < 0 ? -k : k;
  let base = k < 0 ? { x: point.x, y: mod(-point.y, curve.P), isInfinity: false } : point;
  let result = infinityPoint;
  // Double-and-add for efficiency
  while (n > 0) {
    if (n & 1) result = addPoints(result, base, curve);
    base = addPoints(base, base, curve);
    n >>= 1;
  }
  return result;
}

export function findAllPoints(A, B, P) {
  const points = [infinityPoint];
  for (let x = 0; x < P; x += 1) {
    const rhs = mod(x ** 3 + A * x + B, P);
    for (let y = 0; y < P; y += 1) {
      if (mod(y * y, P) === rhs) {
        points.push({ x, y, isInfinity: false });
      }
    }
  }
  return points;
}

export function formatPoint(p) {
  return p.isInfinity ? "O" : `(${p.x}, ${p.y})`;
}

export function buildGeneratorRows(points, curve) {
  const groupOrder = points.length;
  const headers = ["P", ...Array.from({ length: groupOrder }, (_, i) => `[${i + 1}]P`), "order", "generator?"];
  const rows = [];

  points.forEach((p) => {
    const label = formatPoint(p);
    if (p.isInfinity) {
      rows.push([label, ...Array(groupOrder).fill("O"), 1, ""]);
      return;
    }

    const multiples = [];
    let acc = infinityPoint;
    let order = groupOrder;
    for (let k = 1; k <= groupOrder; k += 1) {
      acc = addPoints(acc, p, curve);
      multiples.push(formatPoint(acc));
      if (acc.isInfinity) {
        order = k;
        break;
      }
    }
    while (multiples.length < groupOrder) multiples.push("—");
    const isGenerator = order === groupOrder ? "yes" : "";
    rows.push([label, ...multiples, order, isGenerator]);
  });

  return { headers, rows };
}
