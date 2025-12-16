# Finite Fields & Elliptic Curves Playground (web)

Interactive single-page tool for experimenting with small finite fields and short Weierstrass elliptic curves over F_p. Everything required to run lives in this `web/` folder.

## Features
- Multiplication table for the multiplicative group of integers modulo a chosen prime.
- Element orders and generator detection for Z\*_p.
- Point enumeration on E: y² = x³ + Ax + B over F_p (with singular-curve guardrails).
- Scalar multiples table for each point, highlighting generators.
- Discrete curve plot: canvas grid showing points plus a smooth real-curve overlay for intuition.

## Quick theory refresher
- Over a finite field F_p the “curve” is the set of lattice points (x, y) with y² ≡ x³ + Ax + B (mod p), plus one extra element O (the point at infinity).
- Group law: adding points uses the usual elliptic-curve formulas but all arithmetic is done modulo p; O is the identity.
- The smooth line on the canvas is **not** part of the finite-field group. It is the same equation plotted over the reals to give geometric intuition; only the blue dots are the actual F_p points.
- A curve is singular (and rejected) when 4A³ + 27B² ≡ 0 (mod p); then the group law breaks.

## Running locally
1. Open `index.html` directly in a modern browser, or serve the folder:
   - Python 3: `python -m http.server 8000`
   - Node: `npx serve .`
2. Use small primes (start with `p = 7`) and tweak `A`, `B` to see different curves.

## Inputs and limits
- `p` must be prime and at least 3.
- Singular curves (where `4A³ + 27B² ≡ 0 (mod p)`) are rejected.
- Point enumeration is capped at 60 points to keep tables and the canvas readable.

## Code structure
- `main.js` wires up events, validation, and renders results.
- `utils.js` arithmetic helpers (`mod`, primality, modular inverse).
- `finiteField.js` field-specific computations (tables, element orders).
- `ellipticCurve.js` point arithmetic and scalar multiplication helpers.
- `curveDrawing.js` canvas renderer for the discrete curve grid.
- `dom.js` lightweight DOM utilities for tables and chips.
- `style.css` theme and layout; `index.html` contains the UI scaffolding.

## Notes
- The canvas uses the same coordinate orientation as the tables: `(0,0)` is bottom-left of the grid.
- Resize the window and the plot resizes automatically while preserving sharpness on high-DPI screens.
