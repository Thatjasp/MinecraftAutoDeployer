document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("startButton");
  startButton.addEventListener("click", startServer);
  loadVersions();
});

async function loadVersions() {
  const versionSelect = document.getElementById("version");
  versionSelect.innerHTML = `<option disabled selected>Loading versions...</option>`;

  try {
    // Fetch version list from backend or static file
    const response = await fetch("https://launchermeta.mojang.com/mc/game/version_manifest.json"); // <-- You can replace this with your backend endpoint
    if (!response.ok) throw new Error("Failed to fetch version list");

    const versions = await response.json();
    versionSelect.innerHTML = ""; // clear loading text


    filteredVersionArr = versions.versions.filter((minecraftObj) => {
      return minecraftObj.type == "release";
    });
    filteredVersionArr.forEach(version => {
      const option = document.createElement("option");
      option.value = version.id;
      option.textContent = `Minecraft ${version.id}`;
      versionSelect.appendChild(option);
    });
  } catch (err) {
    versionSelect.innerHTML = `<option disabled>Error loading versions</option>`;
    console.error(err);
  }
}

async function startServer() {
  const version = document.getElementById("version").value;
  const edition = document.getElementById("edition").value;
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

