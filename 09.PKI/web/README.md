PKI / network graph UI (web folder)

Run locally
1) From project root: `cd web && python3 -m http.server 8000`
2) Open http://localhost:8000/index.html in a browser (or open the file directly).

Files
- `index.html` – markup and Vue wiring (structure/layout toggles, form bindings).
- `style.css` – dark theme styling, layout, hover/selection states.
- `core.js` – Vue app state + behaviors (add/delete nodes, parent changes, connectivity checks).
- `visual.js` – D3 rendering (force/tree layouts, selection/path highlighting).
- `utils.js` – pure helpers (cloning, type computation, path/graph utilities).
