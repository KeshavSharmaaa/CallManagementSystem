async function loadFollowUps() {
  const followups = await apiRequest("/salesperson/followups");
  const container = document.getElementById("followupList");

  followups.forEach(f => {
    const div = document.createElement("div");
    div.className = "list-item";
    div.innerHTML = `
      <div>
        <strong>${f.leadName}</strong><br>
        Follow-up at: ${new Date(f.scheduledTime).toLocaleString()}
      </div>
      <button onclick="completeFollowUp('${f._id}')">Done</button>
    `;
    container.appendChild(div);
  });
}

async function completeFollowUp(id) {
  await apiRequest(`/followups/${id}`, "PUT", { completed: true });
  location.reload();
}

loadFollowUps();
