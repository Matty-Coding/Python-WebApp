const countdownEl = document.getElementById("timer");
let remaining = parseInt(countdownEl.textContent.trim()) || 0;

const interval = setInterval(() => {
  if (remaining > 0) {
    remaining--;
    countdownEl.textContent = remaining;
  } else {
    clearInterval(interval);
    window.location.reload();
  }
}, 1000);