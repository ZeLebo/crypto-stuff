import { linkKey, normId } from './utils.js';

const colors = {
  root: '#ff6b6b',
  intermediate: '#5c7cfa',
  leaf: '#2dd4bf'
};

export function renderGraph({ svgSelector, nodes, links, layout, structure, selectedId, highlight, onSelect }) {
  const svg = d3.select(svgSelector);
  const width = 960;
  const height = 620;
  svg.attr('viewBox', `0 0 ${width} ${height}`);
  svg.selectAll('*').remove();

  // isolate data so d3 mutations don't touch Vue state
  const localNodes = nodes.map(n => ({ ...n }));
  const localLinks = links.map(l => ({ source: normId(l.source), target: normId(l.target) }));
  const highlightedNodes = new Set(highlight?.nodes || []);
  const highlightedLinks = new Set((highlight?.links || []).map(linkKey));
  const unreachableRoots = new Set(highlight?.unreachableRoots || []);

  const roots = localNodes.filter(n => n.type === 'root');
  const hasRoots = roots.length > 0;

  if (layout === 'tree' && structure === 'hierarchy' && hasRoots) {
    const virtualRootId = '__virtual_root__';
    const anchorRootId = roots.length === 1 ? roots[0].id : virtualRootId;
    const treeNodes = roots.length === 1 ? localNodes : [...localNodes, { id: virtualRootId, type: 'root', subject: '' }];
    const treeLinks = roots.length === 1 ? localLinks : [...localLinks, ...roots.map(r => ({ source: virtualRootId, target: r.id }))];

    const map = new Map(treeNodes.map(n => [n.id, n]));
    const childrenMap = new Map();
    treeLinks.forEach(l => {
      if (!childrenMap.has(l.source)) childrenMap.set(l.source, []);
      childrenMap.get(l.source).push(l.target);
    });
    function build(id) {
      const node = map.get(id);
      const obj = { data: node, children: [] };
      const ch = childrenMap.get(id) || [];
      ch.forEach(cid => obj.children.push(build(cid)));
      if (!obj.children.length) delete obj.children;
      return obj;
    }
    const hierarchy = d3.hierarchy(build(anchorRootId));
    const treeLayout = d3.tree().size([width - 160, height - 120]);
    treeLayout(hierarchy);

    const nodeById = new Map();
    hierarchy.each(d => {
      nodeById.set(d.data.data.id, { x: d.x + 60, y: d.y + 40 });
    });

    const treeLinksDraw = [];
    hierarchy.each(d => {
      if (d.parent) treeLinksDraw.push({ source: d.parent.data.data.id, target: d.data.data.id });
    });

    svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(treeLinksDraw.filter(l => l.source !== virtualRootId && l.target !== virtualRootId))
      .join('line')
      .attr('class', d => `link ${highlightedLinks.has(linkKey(d)) ? 'path' : ''}`)
      .attr('stroke-width', 2)
      .attr('x1', d => nodeById.get(d.source).x)
      .attr('y1', d => nodeById.get(d.source).y)
      .attr('x2', d => nodeById.get(d.target).x)
      .attr('y2', d => nodeById.get(d.target).y);

    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(localNodes)
      .join('g')
      .attr('class', 'node')
      .attr('transform', d => {
        const p = nodeById.get(d.id) || { x: 50 + Math.random() * (height - 100), y: 80 + Math.random() * (width - 160) };
        return `translate(${p.x},${p.y})`;
      });

    node.append('circle')
      .attr('r', d => d.type === 'root' ? 16 : d.type === 'intermediate' ? 12 : 9)
      .attr('fill', d => colors[d.type] || '#9ca3af');

    node.append('text')
      .attr('x', 12)
      .attr('y', 4)
      .text(d => d.id);

    node.on('click', (event, d) => {
      event.stopPropagation();
      onSelect?.(d.id);
    });

    svg.selectAll('.node')
      .classed('selected', d => d.id === selectedId)
      .classed('path', d => highlightedNodes.has(d.id))
      .classed('unreachable-root', d => unreachableRoots.has(d.id));
    return;
  }

  const simulation = d3.forceSimulation(localNodes)
    .alpha(0.15)
    .alphaDecay(0.05)
    .velocityDecay(0.6)
    .force('link', d3.forceLink(localLinks).id(d => d.id).distance(140))
    .force('charge', d3.forceManyBody().strength(-320))
    .force('collide', d3.forceCollide().radius(36))
    .force('center', d3.forceCenter(width / 2, height / 2));

  const link = svg.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(localLinks)
    .join('line')
    .attr('class', d => `link ${highlightedLinks.has(linkKey(d)) ? 'path' : ''}`)
    .attr('stroke-width', 2);

  const node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(localNodes)
    .join('g')
    .attr('class', 'node')
    .call(drag(simulation));

  node.append('circle')
    .attr('r', d => d.type === 'root' ? 16 : d.type === 'intermediate' ? 12 : 9)
    .attr('fill', d => colors[d.type] || '#9ca3af');

  node.append('text')
    .attr('x', 12)
    .attr('y', 4)
    .text(d => d.id);

  node.on('click', (event, d) => {
    event.stopPropagation();
    onSelect?.(d.id);
  });

  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node.attr('transform', d => `translate(${d.x},${d.y})`)
      .classed('selected', d => d.id === selectedId)
      .classed('path', d => highlightedNodes.has(d.id))
      .classed('unreachable-root', d => unreachableRoots.has(d.id));
  });

  // let the simulation settle once
  simulation.alpha(0.05);
}

export function updateHighlight({ svgSelector, selectedId, highlight }) {
  const svg = d3.select(svgSelector);
  const highlightedNodes = new Set(highlight?.nodes || []);
  const highlightedLinks = new Set((highlight?.links || []).map(linkKey));
  const unreachableRoots = new Set(highlight?.unreachableRoots || []);

  svg.selectAll('.node')
    .classed('selected', d => d.id === selectedId)
    .classed('path', d => highlightedNodes.has(d.id))
    .classed('unreachable-root', d => unreachableRoots.has(d.id));

  svg.selectAll('.link')
    .classed('path', d => highlightedLinks.has(linkKey(d)));
}

function drag(sim) {
  function dragstarted(event, d) {
    if (!event.active) sim.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
  }
  function dragged(event, d) {
    d.fx = event.x; d.fy = event.y;
  }
  function dragended(event, d) {
    if (!event.active) sim.alphaTarget(0);
    d.fx = null; d.fy = null;
  }
  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);
}
