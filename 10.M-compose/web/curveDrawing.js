// Basic discrete plotter for elliptic curve points on F_p
export function drawCurve(points, curve, canvas, highlightPoint, options = {}) {
  const ctx = canvas.getContext("2d");
  const { A, B, P } = curve;
  const width = canvas.width;
  const height = canvas.height;
  const padding = 30;
  // Overlay is just a real-number guide; dots are the actual F_p points
  const showRealOverlay = options.showBackdrop !== false;
  ctx.clearRect(0, 0, width, height);

  if (!Number.isFinite(P) || P <= 1 || !points || points.length === 0) {
    drawMessage(ctx, width, height, "Enter valid A, B, P");
    return [];
  }

  const minCoord = -P;
  const maxCoord = P;
  const range = maxCoord - minCoord;
  const scaleX = (width - padding * 2) / Math.max(1, range);
  const scaleY = (height - padding * 2) / Math.max(1, range);

  const domain = { min: minCoord, max: maxCoord };
  drawGrid(ctx, { P, ...domain }, padding, scaleX, scaleY, width, height);
  if (showRealOverlay) drawRealCurve(ctx, { A, B, ...domain }, padding, scaleX, scaleY);

  const positions = projectPoints(points, domain, padding, scaleX, scaleY);
  drawPoints(ctx, positions, P);
  if (highlightPoint) drawHighlight(ctx, positions, highlightPoint);
  return positions;
}

function drawGrid(ctx, domain, padding, scaleX, scaleY, width, height) {
  const { min, max, P } = domain;
  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,0.06)";
  ctx.fillStyle = "rgba(255,255,255,0.32)";
  ctx.lineWidth = 1;

  for (let i = min; i <= max; i += 1) {
    const x = padding + (i - min) * scaleX;
    const y = padding + (max - i) * scaleY;

    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, height - padding);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(width - padding, y);
    ctx.stroke();

    ctx.font = "10px monospace";
    ctx.fillText(i, x - 5, height - padding + 12);
    ctx.fillText(i, padding - 18, y + 4);
  }

  // axes
  ctx.strokeStyle = "rgba(255,255,255,0.25)";
  ctx.lineWidth = 1.2;
  const zeroX = padding + (0 - min) * scaleX;
  const zeroY = padding + (max - 0) * scaleY;
  ctx.beginPath();
  ctx.moveTo(zeroX, padding);
  ctx.lineTo(zeroX, height - padding);
  ctx.moveTo(padding, zeroY);
  ctx.lineTo(width - padding, zeroY);
  ctx.stroke();

  ctx.restore();
}

function drawMessage(ctx, width, height, message) {
  ctx.save();
  ctx.fillStyle = "rgba(255,255,255,0.7)";
  ctx.font = "14px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(message, width / 2, height / 2);
  ctx.restore();
}

function drawRealCurve(ctx, curve, padding, scaleX, scaleY) {
  const { A, B, min, max } = curve;
  const steps = Math.max(400, (max - min) * 12);
  ctx.save();
  ctx.strokeStyle = "rgba(108,163,255,0.42)";
  ctx.lineWidth = 1.5;

  const strokeBranch = (sign) => {
    ctx.beginPath();
    let started = false;
    for (let i = 0; i < steps; i += 1) {
      const x = min + ((max - min) * i) / (steps - 1);
      const y2 = x * x * x + A * x + B;
      if (y2 < 0) {
        if (started) {
          ctx.stroke();
          ctx.beginPath();
          started = false;
        }
        continue;
      }
      const y = Math.sqrt(y2) * sign;
      const scaledY = y;
      if (scaledY < min || scaledY > max) {
        if (started) {
          ctx.stroke();
          ctx.beginPath();
          started = false;
        }
        continue;
      }
      const cx = padding + (x - min) * scaleX;
      const cy = padding + (max - scaledY) * scaleY;
      if (!started) {
        ctx.moveTo(cx, cy);
        started = true;
      } else {
        ctx.lineTo(cx, cy);
      }
    }
    if (started) ctx.stroke();
  };

  strokeBranch(1);
  strokeBranch(-1);
  ctx.restore();
}

function projectPoints(points, domain, padding, scaleX, scaleY) {
  const { min, max } = domain;
  return points
    .filter((p) => !p.isInfinity)
    .map((p) => ({
      point: p,
      x: padding + (p.x - min) * scaleX,
      y: padding + (max - p.y) * scaleY,
    }));
}

function drawPoints(ctx, projectedPoints, P) {
  ctx.save();
  ctx.fillStyle = "#6ca3ff";
  ctx.strokeStyle = "rgba(255,255,255,0.65)";
  const radius = Math.max(3, 10 / Math.max(4, P));
  projectedPoints.forEach(({ x, y }) => {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  });
  ctx.restore();
}

function drawHighlight(ctx, projectedPoints, highlightPoint) {
  const target = projectedPoints.find(
    ({ point }) => point.x === highlightPoint.x && point.y === highlightPoint.y,
  );
  if (!target) return;
  ctx.save();
  ctx.strokeStyle = "#ffc857";
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.arc(target.x, target.y, 10, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}
