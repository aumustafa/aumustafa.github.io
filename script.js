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

function animate() {
  // Draw translucent black rectangle over entire canvas (fades out old squares)
  ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'; // white with low alpha
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (drawSquare) {
    ctx.fillStyle = 'DarkOrange';
    ctx.fillRect(mouseX - 5, mouseY - 5, 10, 10);
    drawSquare = false;
  }

  requestAnimationFrame(animate);
}

animate();
