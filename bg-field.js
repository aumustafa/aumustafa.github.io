// Ambient background: a dense scatter of tiny dots, a handful of them
// trailing short arced comet tails, all orbiting together — slowly —
// around a fixed pivot point near the bottom of the screen. The canvas
// itself stays fully transparent; this never paints over the page's real
// background. Skips entirely if the user prefers reduced motion (see the
// media query in bg-field.css).
(function () {
  const canvas = document.getElementById('bg-field');
  if (!canvas || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');
  const style = getComputedStyle(canvas);
  const dotColor = style.getPropertyValue('--dot-color').trim() || '#ffffff';

  let width, height, dpr;
  let shapes = [];
  let pivot = { x: 0, y: 0 };

  const SHAPE_COUNT = 2000;
  const COMET_FRACTION = 0.01; // ~6% of dots trail a tail
  const ROTATION_PERIOD_MS = 360000 * 2; // one full orbit every 3 minutes — deliberately slow
  const ANGULAR_SPEED = (Math.PI * 2) / ROTATION_PERIOD_MS;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Pivot sits off-screen, past the bottom-right corner — shapes sweep
    // through the visible area like a slow radar turning from just outside
    // the frame, rather than a symmetric decoration centered on the page.
    pivot = { x: width * 1.15, y: height * 1.12 };

    // Only radii that can actually intersect the visible rectangle at some
    // angle are worth placing shapes at. minRadius = distance to the nearest
    // point on the screen rect; maxRadius = distance to the farthest corner.
    const clampedX = Math.min(Math.max(pivot.x, 0), width);
    const clampedY = Math.min(Math.max(pivot.y, 0), height);
    const minRadius = Math.hypot(pivot.x - clampedX, pivot.y - clampedY);
    const corners = [
      [0, 0], [width, 0], [0, height], [width, height],
    ];
    const maxRadius = Math.max(
      ...corners.map(([cx, cy]) => Math.hypot(pivot.x - cx, pivot.y - cy))
    );

    shapes = Array.from({ length: SHAPE_COUNT }, () => {
      const isComet = Math.random() < COMET_FRACTION;
      return {
        angle: Math.random() * Math.PI * 2,
        radius: minRadius + Math.random() * (maxRadius - minRadius),
        isComet,
        // Angular length of the trailing tail, in radians — only set for comets.
        tailSpan: isComet ? 0.12 + Math.random() * 0.26 : 0,
        size: isComet ? Math.random() * 1.0 + 0.9 : Math.random() * 0.8 + 0.35,
        opacity: isComet
          ? Math.random() * 0.25 + 0.5
          : Math.random() * 0.15 + 0.5,
      };
    });
  }

  function drawDot(x, y, size, opacity) {
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.globalAlpha = opacity;
    ctx.fillStyle = dotColor;
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  // Draws a short curved tail trailing behind the dot along its own
  // orbital arc (rather than a straight line), fading out toward the tip.
  function drawCometTail(cx, cy, radius, headAngle, tailSpan, size, baseOpacity) {
    const segments = 10;
    for (let i = 0; i < segments; i++) {
      const t0 = i / segments;
      const t1 = (i + 1) / segments;
      const a0 = headAngle - tailSpan * t0;
      const a1 = headAngle - tailSpan * t1;
      const x0 = cx + Math.cos(a0) * radius;
      const y0 = cy + Math.sin(a0) * radius;
      const x1 = cx + Math.cos(a1) * radius;
      const y1 = cy + Math.sin(a1) * radius;

      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.globalAlpha = baseOpacity * (1 - t1);
      ctx.strokeStyle = dotColor;
      ctx.lineWidth = size * 0.55;
      ctx.lineCap = 'round';
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function draw(time) {
    ctx.clearRect(0, 0, width, height);
    const rotation = time * ANGULAR_SPEED;

    for (const s of shapes) {
      const a = s.angle + rotation;
      const x = pivot.x + Math.cos(a) * s.radius;
      const y = pivot.y + Math.sin(a) * s.radius;

      if (s.isComet) {
        drawCometTail(pivot.x, pivot.y, s.radius, a, s.tailSpan, s.size, s.opacity);
      }
      drawDot(x, y, s.size, s.opacity);
    }

    requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener('resize', resize);
  requestAnimationFrame(draw);
})();