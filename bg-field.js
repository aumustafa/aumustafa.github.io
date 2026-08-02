// Ambient background: a sparse scatter of dots and small star shapes,
// all orbiting together — slowly — around a fixed pivot point near the
// bottom of the screen. The canvas itself stays fully transparent; this
// never paints over the page's real background. Skips entirely if the
// user prefers reduced motion (see the media query in bg-field.css).
(function () {
  const canvas = document.getElementById('bg-field');
  if (!canvas || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');
  const style = getComputedStyle(canvas);
  const dotColor = style.getPropertyValue('--dot-color').trim() || '#ffffff';
  const starColor = style.getPropertyValue('--star-color').trim() || '#ffffff';

  let width, height, dpr;
  let shapes = [];
  let pivot = { x: 0, y: 0 };

  const SHAPE_COUNT = 300;
  const ROTATION_PERIOD_MS = 180000; // one full orbit every 3 minutes — deliberately slow
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

    shapes = Array.from({ length: SHAPE_COUNT }, () => ({
      angle: Math.random() * Math.PI * 2,
      radius: minRadius + Math.random() * (maxRadius - minRadius),
      type: Math.random() < 0.35 ? 'star' : 'dot',
      size: Math.random() * 2.4 + 1.2,
      opacity: Math.random() * 0.35 + 0.15,
    }));
  }

  function drawDot(x, y, size, opacity) {
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.globalAlpha = opacity;
    ctx.fillStyle = dotColor;
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  function drawStar(x, y, size, opacity, rotation) {
    const spikes = 4;
    const outerR = size * 2.6;
    const innerR = outerR * 0.4;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);
    ctx.beginPath();
    for (let i = 0; i < spikes * 2; i++) {
      const r = i % 2 === 0 ? outerR : innerR;
      const a = (Math.PI / spikes) * i;
      const px = Math.cos(a) * r;
      const py = Math.sin(a) * r;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.globalAlpha = opacity;
    ctx.fillStyle = starColor;
    ctx.fill();
    ctx.restore();
    ctx.globalAlpha = 1;
  }

  function draw(time) {
    ctx.clearRect(0, 0, width, height);
    const rotation = time * ANGULAR_SPEED;

    for (const s of shapes) {
      const a = s.angle + rotation;
      const x = pivot.x + Math.cos(a) * s.radius;
      const y = pivot.y + Math.sin(a) * s.radius;

      if (s.type === 'star') {
        drawStar(x, y, s.size, s.opacity, a);
      } else {
        drawDot(x, y, s.size, s.opacity);
      }
    }

    requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener('resize', resize);
  requestAnimationFrame(draw);
})();