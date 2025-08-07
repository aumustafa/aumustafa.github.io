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


// function animate() {
//   // Draw translucent black rectangle over entire canvas (fades out old squares)
//   ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'; // white with low alpha
//   ctx.fillRect(0, 0, canvas.width, canvas.height);

//   if (drawSquare) {
//     ctx.fillStyle = 'DarkOrange';
//     ctx.fillRect(mouseX - 5, mouseY - 5, 10, 10);
//     drawSquare = false;
//   }

//   requestAnimationFrame(animate);
// }

const cellSize = 10;
let lastCellX = -1;
let lastCellY = -1;
let hue = 30; // start near 'DarkOrange'

function animate() {
  ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
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
  const easedRatio = Math.pow(ratio, 1.5)

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

  requestAnimationFrame(animate);
}


animate();
