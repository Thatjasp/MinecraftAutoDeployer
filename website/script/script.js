document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("startButton");
  startButton.addEventListener("click", startServer);
});

async function startServer() {
  const version = document.getElementById("version").value;
  const status = document.getElementById("status");
  status.textContent = "Starting server...";

  try {
    const response = await fetch("/start-minecraft", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ version })
    });

    if (response.ok) {
      const data = await response.json();
      status.textContent = `✅ Server started: ${data.message || "Success"}`;
    } else {
      const err = await response.text();
      status.textContent = `❌ Error: ${err}`;
    }
  } catch (e) {
    status.textContent = `❌ Network error: ${e.message}`;
  }
}

