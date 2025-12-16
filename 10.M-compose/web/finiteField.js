import { mod } from "./utils.js";

export function buildMultiplicationTable(p) {
  const elements = Array.from({ length: p - 1 }, (_, i) => i + 1);
  const headers = ["×", ...elements];
  const rows = elements.map((i) => [i, ...elements.map((j) => mod(i * j, p))]);
  return { headers, rows };
}

export function elementOrder(a, p) {
  let power = a;
  let k = 1;
  while (power !== 1) {
    power = mod(power * a, p);
    k += 1;
    if (k > p + 2) break; // safety guard
  }
  return k;
}

export function buildOrderRows(p) {
  const elements = Array.from({ length: p - 1 }, (_, i) => i + 1);
  const rows = elements.map((a) => {
    const order = elementOrder(a, p);
    const sequence = [];
    let current = 1;
    for (let i = 0; i < order; i += 1) {
      sequence.push(current);
      current = mod(current * a, p);
    }
    const isGenerator = order === p - 1 ? "yes" : "";
    return [a, order, isGenerator, sequence.join(" → ")];
  });
  return rows;
}
