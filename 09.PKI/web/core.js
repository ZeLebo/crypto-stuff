import { cloneData, computeTypes, getParentId, pathToRoot, pathBetween, linksFromPath, buildParentMap } from './utils.js';
import { renderGraph, updateHighlight } from './visual.js';

const sample = {
  nodes: [
    { id: 'Root CA', subject: 'CN=Root CA, O=Example' },
    { id: 'Intermediate A', subject: 'CN=Intermediate A, O=Example' },
    { id: 'Intermediate B', subject: 'CN=Intermediate B, O=Example' },
    { id: 'Leaf 1', subject: 'CN=www.example.com' },
    { id: 'Leaf 2', subject: 'CN=api.example.com' },
    { id: 'Leaf 3', subject: 'CN=mail.example.com' }
  ],
  links: [
    { source: 'Root CA', target: 'Intermediate A' },
    { source: 'Root CA', target: 'Intermediate B' },
    { source: 'Intermediate A', target: 'Leaf 1' },
    { source: 'Intermediate A', target: 'Leaf 2' },
    { source: 'Intermediate B', target: 'Leaf 3' }
  ]
};

const { createApp } = Vue;

createApp({
  data() {
    const { nodes, links } = cloneData(sample);
    return {
      nodes,
      links,
      layout: 'force',
      structure: 'hierarchy',
      selectedId: null,
      editSubject: '',
      editParent: '',
      targetId: '',
      newNode: { id: '', parent: '' },
      checkResult: '',
      highlight: { nodes: [], links: [] },
      needsRender: true,
      lastLayoutKey: ''
    };
  },
  computed: {
    parentOptions() {
      return this.nodes.map(n => n.id);
    },
    selectedNode() {
      return this.nodes.find(n => n.id === this.selectedId) || null;
    },
    checkResultState() {
      if (!this.checkResult) return '';
      const text = this.checkResult.toLowerCase();
      return text.includes('not') || text.includes('no path') ? 'warn' : 'ok';
    }
  },
  mounted() {
    this.refreshTypes();
    this.draw();
  },
  methods: {
    refreshTypes() {
      this.nodes = computeTypes(this.nodes, this.links);
    },
    draw() {
      this.refreshTypes();
      const layoutKey = `${this.layout}|${this.structure}|${JSON.stringify(this.links)}|${this.nodes.length}`;
      if (this.needsRender || layoutKey !== this.lastLayoutKey) {
        renderGraph({
          svgSelector: '#graph',
          nodes: this.nodes,
          links: this.links,
          layout: this.layout,
          structure: this.structure,
          selectedId: this.selectedId,
          highlight: this.highlight,
          onSelect: id => this.selectNode(id)
        });
        this.lastLayoutKey = layoutKey;
        this.needsRender = false;
      }
      updateHighlight({
        svgSelector: '#graph',
        selectedId: this.selectedId,
        highlight: this.highlight
      });
    },
    resetSample() {
      const { nodes, links } = cloneData(sample);
      this.nodes = nodes;
      this.links = links;
      this.selectedId = null;
      this.editSubject = '';
      this.editParent = '';
      this.targetId = '';
      this.checkResult = '';
      this.highlight = { nodes: [], links: [] };
      this.needsRender = true;
      this.draw();
    },
    addNode() {
      const id = this.newNode.id.trim();
      if (!id) return alert('Provide new node id');
      if (this.nodes.find(n => n.id === id)) return alert('Node id already exists');
      this.nodes.push({ id, subject: '' });
      if (this.newNode.parent) this.links.push({ source: this.newNode.parent, target: id });
      this.newNode.id = '';
      this.newNode.parent = '';
      this.checkResult = '';
      this.highlight = { nodes: [], links: [] };
      this.needsRender = true;
      this.draw();
    },
    deleteSelected() {
      if (!this.selectedId) return alert('Select a node to delete');
      this.nodes = this.nodes.filter(n => n.id !== this.selectedId);
      this.links = this.links.filter(l => l.source !== this.selectedId && l.target !== this.selectedId);
      this.selectedId = null;
      this.editSubject = '';
      this.editParent = '';
      this.targetId = '';
      this.checkResult = '';
      this.highlight = { nodes: [], links: [] };
      this.needsRender = true;
      this.draw();
    },
    changeSubject() {
      if (!this.selectedId) return alert('Select a node first');
      const node = this.nodes.find(n => n.id === this.selectedId);
      if (!node) return;
      node.subject = this.editSubject;
      this.needsRender = false;
      this.draw();
    },
    updateParent() {
      if (!this.selectedId) return;
      if (this.editParent === this.selectedId) return alert('Cannot parent a node to itself.');

      // remove existing parents for the selected node
      this.links = this.links.filter(l => l.target !== this.selectedId);

      if (this.editParent) this.links.push({ source: this.editParent, target: this.selectedId });

      // ensure at least one root remains; if none, detach the chosen parent from its own parent
      const parents = buildParentMap(this.links);
      const hasRoot = this.nodes.some(n => !parents.has(n.id));
      if (!hasRoot && this.editParent) {
        this.links = this.links.filter(l => l.target !== this.editParent);
      }

      this.checkResult = '';
      this.highlight = { nodes: [], links: [] };
      this.needsRender = true;
      this.draw();
    },
    checkConnectivity() {
      if (!this.selectedId) return alert('Select a node to check');
      this.highlight = { nodes: [], links: [] };

      if (this.structure === 'hierarchy') {
        const parents = buildParentMap(this.links);
        const roots = this.nodes.filter(n => n.type === 'root').map(n => n.id);
        const reachablePaths = [];
        const unreachableRoots = [];

        roots.forEach(rootId => {
          const path = pathToSpecificRoot(this.selectedId, rootId, parents);
          if (path.length) {
            reachablePaths.push(path);
          } else {
            unreachableRoots.push(rootId);
          }
        });

        const pathNodes = new Set();
        const pathLinks = [];
        reachablePaths.forEach(p => {
          p.forEach(n => pathNodes.add(n));
          linksFromPath(p, this.links).forEach(l => pathLinks.push(l));
        });

        this.highlight = { nodes: Array.from(pathNodes), links: pathLinks, unreachableRoots };
        const msgParts = [];
        if (reachablePaths.length) msgParts.push(`reachable roots: ${reachablePaths.map(p => p[p.length - 1]).join(', ')}`);
        if (unreachableRoots.length) msgParts.push(`unreachable: ${unreachableRoots.join(', ')}`);
        this.checkResult = msgParts.length ? msgParts.join(' | ') : 'No roots found.';
      } else {
        if (!this.targetId) return alert('Choose a target node to find a path');
        const path = pathBetween(this.selectedId, this.targetId, this.links);
        if (path.length > 0) {
          this.highlight = { nodes: path, links: linksFromPath(path, this.links) };
          this.checkResult = `Path found: ${path.join(' → ')}`;
        } else {
          this.checkResult = `No path between ${this.selectedId} and ${this.targetId}.`;
        }
      }
      this.draw();
    },
    selectNode(id) {
      this.selectedId = id;
      this.editSubject = this.selectedNode?.subject || '';
      this.editParent = getParentId(this.links, id);
      this.targetId = '';
      this.checkResult = '';
      this.highlight = { nodes: [], links: [] };
      this.needsRender = false;
      this.draw();
    }
  },
  watch: {
    layout() {
      this.draw();
    },
    structure() {
      if (this.structure !== 'hierarchy' && this.layout === 'tree') {
        this.layout = 'force';
      }
      this.highlight = { nodes: [], links: [] };
      this.checkResult = '';
      this.draw();
    }
  }
}).mount('#app');

function pathToSpecificRoot(startId, rootId, parents) {
  const visited = new Set();
  const path = [];
  let cur = startId;
  while (cur && !visited.has(cur)) {
    path.push(cur);
    if (cur === rootId) return path;
    visited.add(cur);
    if (!parents.has(cur)) return [];
    cur = parents.get(cur);
  }
  return [];
}
