// Utility helpers for PKI graph logic

export function normId(value) {
  return typeof value === 'object' && value !== null ? value.id : value;
}

export function cloneData(data) {
  return {
    nodes: data.nodes.map(n => ({ ...n })),
    links: data.links.map(l => ({ source: normId(l.source), target: normId(l.target) }))
  };
}

export function linkKey(d) {
  const s = normId(d.source);
  const t = normId(d.target);
  return `${s}-->${t}`;
}

export function buildParentMap(links) {
  const parents = new Map();
  links.forEach(l => parents.set(normId(l.target), normId(l.source)));
  return parents;
}

export function buildChildrenMap(links) {
  const children = new Map();
  links.forEach(l => {
    const s = normId(l.source);
    const t = normId(l.target);
    if (!children.has(s)) children.set(s, []);
    children.get(s).push(t);
  });
  return children;
}

export function computeTypes(nodes, links) {
  const parents = buildParentMap(links);
  const children = buildChildrenMap(links);
  const roots = new Set(nodes.filter(n => !parents.has(n.id)).map(n => n.id));

  return nodes.map(n => {
    if (roots.has(n.id)) return { ...n, type: 'root' };
    if (children.has(n.id)) return { ...n, type: 'intermediate' };
    return { ...n, type: 'leaf' };
  });
}

export function getParentId(links, id) {
  const edge = links.find(l => normId(l.target) === id);
  return edge ? normId(edge.source) : '';
}

export function pathToRoot(startId, links) {
  const parents = buildParentMap(links);
  const visited = new Set();
  const path = [];
  let cur = startId;

  while (cur && !visited.has(cur)) {
    path.push(cur);
    visited.add(cur);
    if (!parents.has(cur)) return path; // reached a root
    cur = parents.get(cur);
  }
  return [];
}

export function pathBetween(a, b, links) {
  if (a === b) return [a];
  const adj = new Map();
  links.forEach(l => {
    const s = normId(l.source);
    const t = normId(l.target);
    if (!adj.has(s)) adj.set(s, []);
    if (!adj.has(t)) adj.set(t, []);
    adj.get(s).push(t);
    adj.get(t).push(s);
  });

  const visited = new Set();
  const queue = [[a]];
  while (queue.length) {
    const path = queue.shift();
    const node = path[path.length - 1];
    if (node === b) return path;
    if (visited.has(node)) continue;
    visited.add(node);
    const neighbors = adj.get(node) || [];
    neighbors.forEach(next => {
      if (!visited.has(next)) queue.push([...path, next]);
    });
  }
  return [];
}

export function linksFromPath(path, links) {
  const pairs = [];
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i];
    const b = path[i + 1];
    const existing = links.find(l =>
      (normId(l.source) === a && normId(l.target) === b) || (normId(l.source) === b && normId(l.target) === a)
    );
    if (existing) {
      pairs.push({ source: normId(existing.source), target: normId(existing.target) });
    } else {
      pairs.push({ source: a, target: b });
    }
  }
  return pairs;
}
