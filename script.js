const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Resize canvas if window changes
window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

let mouseX = 0;
let mouseY = 0;
let drawSquare = false;
let lastDrawTime = 0;
const throttleDelay = 20; // ms

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;

  const now = Date.now();
  if (now - lastDrawTime > throttleDelay) {
    drawSquare = true;
    lastDrawTime = now;
  }
});

document.addEventListener('touchmove', (e) => {
  e.preventDefault(); // prevents scrolling
  const touch = e.touches[0];
  mouseX = touch.clientX;
  mouseY = touch.clientY;
  drawSquare = true;
}, { passive: false });

function drawHand(centerX, centerY, angle, length, color, width) {
  ctx.save(); // Save current state
  ctx.translate(centerX, centerY);
  ctx.rotate(angle);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(0, -length);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.lineCap = 'round';
  ctx.stroke();
  ctx.restore(); // Restore to original state
}

function drawClock() {
  const now = new Date();
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  const minDim = Math.min(canvas.width, canvas.height);
  const hourLength = minDim * 0.3;
  const minuteLength = minDim * 0.4;
  const secondLength = minDim * 0.45;

  const second = now.getSeconds() + now.getMilliseconds() / 1000;
  const minute = now.getMinutes() + second / 60;
  const hour = now.getHours() % 12 + minute / 60;

  const secondAngle = (Math.PI / 30) * second;
  const minuteAngle = (Math.PI / 30) * minute;
  const hourAngle = (Math.PI / 6) * hour;

  drawHand(centerX, centerY, hourAngle, hourLength, '#000', 6);
  drawHand(centerX, centerY, minuteAngle, minuteLength, '#555', 4);
  drawHand(centerX, centerY, secondAngle, secondLength, `hsl(${hue}, 100%, 50%)`, 2);
}

const cellSize = 10;
let lastCellX = -1;
let lastCellY = -1;
let hue = 30; // start near 'DarkOrange'

function animate() {
  ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  // Distance from center (normalized)
  const dx = mouseX - centerX;
  const dy = mouseY - centerY;
  const distance = Math.sqrt(dx * dx + dy * dy);

  // Max possible distance is from center to a corner
  const maxDistance = Math.sqrt(centerX * centerX + centerY * centerY);

  // Ratio: 0 (center) to 1 (corner)
  const ratio = distance / maxDistance;
  const easedRatio = Math.pow(ratio, 2)

  // Map ratio to alpha: 0.1 (in center) to 0.8 (edges)
  const alpha = 0.05 + easedRatio * 0.95;

  // Update ASCII text color
  const asciiDiv = document.getElementById('ascii');
  asciiDiv.style.color = `rgba(0, 0, 0, ${alpha.toFixed(2)})`;

  if (drawSquare) {
    const gridX = Math.floor(mouseX / cellSize) * cellSize;
    const gridY = Math.floor(mouseY / cellSize) * cellSize;

    if (gridX !== lastCellX || gridY !== lastCellY) {
      // Use HSL color
      ctx.fillStyle = `hsl(${hue}, 100%, 60%)`;
      ctx.fillRect(gridX, gridY, cellSize, cellSize);

      // Slowly rotate through the hue wheel
      hue = (hue + 1) % 360;

      lastCellX = gridX;
      lastCellY = gridY;
    }

    drawSquare = false;
  }

  drawClock();
  requestAnimationFrame(animate);
}


animate();
