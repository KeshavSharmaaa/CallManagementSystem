async function loadSalespersons() {
  const salespersons = await apiRequest("/manager/salespersons");
  const select = document.getElementById("salespersonSelect");

  salespersons.forEach(sp => {
    const option = document.createElement("option");
    option.value = sp._id;
    option.textContent = sp.name;
    select.appendChild(option);
  });
}

async function assignLead() {
  const name = document.getElementById("leadName").value;
  const phone = document.getElementById("leadPhone").value;
  const assignedTo = document.getElementById("salespersonSelect").value;

  if (!name || !phone) {
    alert("Fill all fields");
    return;
  }

  await apiRequest("/leads", "POST", {
    name,
    phone,
    assignedTo
  });

  alert("Lead assigned successfully");
}

loadSalespersons();
