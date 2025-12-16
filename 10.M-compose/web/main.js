import { isPrime, mod } from "./utils.js";
import { renderTable, renderChips } from "./dom.js";
import { buildMultiplicationTable, buildOrderRows } from "./finiteField.js";
import { findAllPoints, buildGeneratorRows, formatPoint } from "./ellipticCurve.js";
import { drawCurve } from "./curveDrawing.js";

const fieldPrimeInput = document.getElementById("fieldPrime");
const multiplicationTableEl = document.getElementById("multiplicationTable");
const orderTableEl = document.getElementById("orderTable");

const curveAInput = document.getElementById("curveA");
const curveBInput = document.getElementById("curveB");
const curvePInput = document.getElementById("curveP");
const pointsTarget = document.getElementById("pointsList");
const generatorTarget = document.getElementById("generatorTable");
const curveCanvas = document.getElementById("curveCanvas");
const pointStatus = document.getElementById("pointStatus");
const backdropToggle = document.getElementById("toggleBackdrop");

let lastProjectedPoints = [];
let lastCurveParams = null;
let selectedPoint = null;
let lastPointsList = [];
const computePrompt = "Compute the curve to enable point selection.";
const noPointsMessage = "No affine points to click for this curve.";

function computeFieldSection() {
  const p = parseInt(fieldPrimeInput.value, 10);

  if (!Number.isFinite(p) || p < 3) {
    multiplicationTableEl.textContent = "Enter a prime ≥ 3.";
    orderTableEl.textContent = "Enter a prime ≥ 3.";
    return;
  }
  if (!isPrime(p)) {
    multiplicationTableEl.textContent = `${p} is not prime. Try 5, 7, 11…`;
    orderTableEl.textContent = `${p} is not prime.`;
    return;
  }

  const { headers, rows } = buildMultiplicationTable(p);
  renderTable(headers, rows, multiplicationTableEl);

  const orderRows = buildOrderRows(p);
  renderTable(["a", "order", "generator?", "powers until 1"], orderRows, orderTableEl);
}

function computeCurveSection() {
  const A = parseInt(curveAInput.value, 10);
  const B = parseInt(curveBInput.value, 10);
  const P = parseInt(curvePInput.value, 10);
  selectedPoint = null;
  lastPointsList = [];

  // Validation chain: inputs -> prime -> discriminant -> size
  if (![A, B, P].every(Number.isFinite)) {
    pointsTarget.textContent = "Enter numeric A, B, P.";
    generatorTarget.textContent = "Enter numeric A, B, P.";
    drawCurve([], { P: 0 }, curveCanvas);
    lastProjectedPoints = [];
    lastCurveParams = null;
    updatePointStatus(computePrompt);
    return;
  }
  if (!isPrime(P)) {
    pointsTarget.textContent = `${P} is not prime.`;
    generatorTarget.textContent = `${P} is not prime.`;
    drawCurve([], { P: 0 }, curveCanvas);
    lastProjectedPoints = [];
    lastCurveParams = null;
    updatePointStatus(computePrompt);
    return;
  }

  const discriminant = mod(4 * (A ** 3) + 27 * (B ** 2), P);
  if (discriminant === 0) {
    pointsTarget.textContent = "Singular curve (4A^3 + 27B^2 ≡ 0 mod P). Pick different A, B.";
    generatorTarget.textContent = "";
    drawCurve([], { P }, curveCanvas);
    lastProjectedPoints = [];
    lastCurveParams = null;
    updatePointStatus(computePrompt);
    return;
  }

  const points = findAllPoints(A, B, P);
  if (points.length > 60) {
    pointsTarget.textContent = `Too many points (${points.length}). Try a smaller prime.`;
    generatorTarget.textContent = "";
    drawCurve([], { P }, curveCanvas);
    lastProjectedPoints = [];
    lastCurveParams = null;
    updatePointStatus(computePrompt);
    return;
  }

  lastPointsList = points;
  renderChips(points.map(formatPoint), pointsTarget, handleChipClick);

  const curve = { A, B, P };
  const { headers, rows } = buildGeneratorRows(points, curve);
  renderTable(headers, rows, generatorTarget);
  lastCurveParams = curve;
  lastProjectedPoints = drawCurve(points, curve, curveCanvas, selectedPoint, {
    showBackdrop: backdropToggle?.checked !== false,
  });
  if (lastProjectedPoints.length === 0) {
    updatePointStatus(noPointsMessage);
  } else {
    updatePointStatus("Click a point to highlight it.");
  }
}

function resizeCanvas() {
  const ratio = window.devicePixelRatio || 1;
  const cssHeight = 320;
  const clientWidth = curveCanvas.clientWidth || curveCanvas.width || 520;
  curveCanvas.width = Math.floor(clientWidth * ratio);
  curveCanvas.height = Math.floor(cssHeight * ratio);
  curveCanvas.style.height = `${cssHeight}px`;
}

function handleChipClick(idx) {
  if (!lastPointsList.length || !lastCurveParams) return;
  const targetPoint = lastPointsList[idx];
  if (!targetPoint || targetPoint.isInfinity) return;
  selectedPoint = targetPoint;
  updatePointStatus(`Selected ${formatPoint(selectedPoint)}.`);
  lastProjectedPoints = drawCurve(lastPointsList, lastCurveParams, curveCanvas, selectedPoint);
}

function handleCanvasClick(evt) {
  if (!lastCurveParams) {
    updatePointStatus(computePrompt);
    return;
  }
  if (!lastProjectedPoints.length) {
    updatePointStatus(noPointsMessage);
    return;
  }
  // Hit-test in device pixels so high-DPI canvases stay clickable
  const rect = curveCanvas.getBoundingClientRect();
  const ratio = curveCanvas.width / rect.width;
  const x = (evt.clientX - rect.left) * ratio;
  const y = (evt.clientY - rect.top) * ratio;
  const baseRadius = Math.max(3, 10 / Math.max(4, lastCurveParams.P));
  const hitRadius = baseRadius * 2.6;

  let closest = null;
  let minDist = Infinity;
  lastProjectedPoints.forEach((pt) => {
    const dx = pt.x - x;
    const dy = pt.y - y;
    const d2 = dx * dx + dy * dy;
    if (d2 < minDist) {
      minDist = d2;
      closest = pt;
    }
  });

  if (!closest || Math.sqrt(minDist) > hitRadius) return;
  selectedPoint = closest.point;
  updatePointStatus(`Selected ${formatPoint(selectedPoint)}.`);
  lastProjectedPoints = drawCurve(
    lastPointsList,
    lastCurveParams,
    curveCanvas,
    selectedPoint,
    { showBackdrop: backdropToggle?.checked !== false },
  );
}

function updatePointStatus(text) {
  if (pointStatus) pointStatus.textContent = text;
}

function init() {
  if (!curveCanvas) return;
  resizeCanvas();
  document.getElementById("computeField").addEventListener("click", computeFieldSection);
  document.getElementById("computeCurve").addEventListener("click", computeCurveSection);
  if (backdropToggle) {
    backdropToggle.addEventListener("change", () => {
      if (!lastCurveParams) return;
      lastProjectedPoints = drawCurve(
        lastPointsList,
        lastCurveParams,
        curveCanvas,
        selectedPoint,
        { showBackdrop: backdropToggle.checked },
      );
    });
  }
  window.addEventListener("resize", resizeCanvas);
  curveCanvas.addEventListener("click", handleCanvasClick);
  computeFieldSection();
  computeCurveSection();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
