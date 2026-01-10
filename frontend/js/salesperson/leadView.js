async function loadLeads() {
  const leads = await apiRequest("/salesperson/leads");
  const container = document.getElementById("leadList");

  leads.forEach(lead => {
    const div = document.createElement("div");
    div.className = "list-item";
    div.innerHTML = `
      <div>
        <strong>${lead.name}</strong><br>
        ${lead.phone}
      </div>
      <a href="call.html?leadId=${lead._id}">Call</a>
    `;
    container.appendChild(div);
  });
}

loadLeads();
