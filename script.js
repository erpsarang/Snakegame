const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const restartButton = document.getElementById("restart");

const gridSize = 20;
const tileSize = canvas.width / gridSize;
const baseSpeed = 10; // moves per second

let snake;
let direction;
let nextDirection;
let apple;
let score;
let speed;
let lastUpdate = 0;
let isPaused = false;
let isGameOver = false;

function init() {
  snake = [
    { x: Math.floor(gridSize / 2), y: Math.floor(gridSize / 2) },
    { x: Math.floor(gridSize / 2) - 1, y: Math.floor(gridSize / 2) },
  ];
  direction = { x: 1, y: 0 };
  nextDirection = { ...direction };
  apple = spawnApple();
  score = 0;
  speed = baseSpeed;
  scoreEl.textContent = score;
  lastUpdate = 0;
  isPaused = false;
  isGameOver = false;
}

function spawnApple() {
  let position;
  do {
    position = {
      x: Math.floor(Math.random() * gridSize),
      y: Math.floor(Math.random() * gridSize),
    };
  } while (snake.some((segment) => segment.x === position.x && segment.y === position.y));
  return position;
}

function update() {
  if (isPaused || isGameOver) {
    return;
  }

  direction = nextDirection;
  const head = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y,
  };

  if (
    head.x < 0 ||
    head.y < 0 ||
    head.x >= gridSize ||
    head.y >= gridSize ||
    snake.some((segment) => segment.x === head.x && segment.y === head.y)
  ) {
    isGameOver = true;
    return;
  }

  snake.unshift(head);

  if (head.x === apple.x && head.y === apple.y) {
    score += 10;
    speed = baseSpeed + Math.floor(score / 50);
    apple = spawnApple();
    scoreEl.textContent = score;
  } else {
    snake.pop();
  }
}

function draw() {
  ctx.fillStyle = "#050505";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
  for (let i = 0; i <= gridSize; i++) {
    ctx.beginPath();
    ctx.moveTo(i * tileSize, 0);
    ctx.lineTo(i * tileSize, canvas.height);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, i * tileSize);
    ctx.lineTo(canvas.width, i * tileSize);
    ctx.stroke();
  }

  const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  gradient.addColorStop(0, "#38ef7d");
  gradient.addColorStop(1, "#11998e");
  ctx.fillStyle = gradient;
  for (const segment of snake) {
    ctx.fillRect(
      segment.x * tileSize + 1,
      segment.y * tileSize + 1,
      tileSize - 2,
      tileSize - 2
    );
  }

  ctx.fillStyle = "#ff4757";
  ctx.beginPath();
  const appleCenterX = apple.x * tileSize + tileSize / 2;
  const appleCenterY = apple.y * tileSize + tileSize / 2;
  const appleRadius = (tileSize - 6) / 2;
  ctx.arc(appleCenterX, appleCenterY, appleRadius, 0, Math.PI * 2);
  ctx.fill();

  if (isGameOver) {
    drawOverlay("Game Over", "Press Restart to play again");
  } else if (isPaused) {
    drawOverlay("Paused", "Press space to continue");
  }
}

function drawOverlay(title, subtitle) {
  ctx.fillStyle = "rgba(0, 0, 0, 0.65)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 32px 'Segoe UI', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(title, canvas.width / 2, canvas.height / 2 - 10);

  ctx.font = "16px 'Segoe UI', sans-serif";
  ctx.fillText(subtitle, canvas.width / 2, canvas.height / 2 + 20);
}

function gameLoop(timestamp) {
  requestAnimationFrame(gameLoop);
  if (!lastUpdate) {
    lastUpdate = timestamp;
  }
  const delta = timestamp - lastUpdate;
  const threshold = 1000 / speed;
  if (delta > threshold) {
    lastUpdate = timestamp - (delta % threshold);
    update();
    draw();
  }
}

function handleInput(event) {
  const key = event.code;

  if (key === "Space") {
    if (!isGameOver) {
      isPaused = !isPaused;
    }
    event.preventDefault();
    return;
  }

  const controls = {
    ArrowUp: { x: 0, y: -1 },
    KeyW: { x: 0, y: -1 },
    ArrowDown: { x: 0, y: 1 },
    KeyS: { x: 0, y: 1 },
    ArrowLeft: { x: -1, y: 0 },
    KeyA: { x: -1, y: 0 },
    ArrowRight: { x: 1, y: 0 },
    KeyD: { x: 1, y: 0 },
  };

  const newDirection = controls[key];
  if (!newDirection) {
    return;
  }

  if (snake.length > 1 && newDirection.x === -direction.x && newDirection.y === -direction.y) {
    return;
  }

  nextDirection = newDirection;
  isPaused = false;
  event.preventDefault();
}

restartButton.addEventListener("click", () => {
  init();
  draw();
});

document.addEventListener("keydown", handleInput);

init();
draw();
requestAnimationFrame(gameLoop);
