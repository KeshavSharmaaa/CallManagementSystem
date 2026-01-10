let allEmployees = [];

async function loadTeamPerformance() {
  const data = await apiRequest("/manager/team-performance");
  const tbody = document.getElementById("teamTable");

  data.forEach(sp => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${sp.name}</td>
      <td>${sp.calls}</td>
      <td>${sp.conversions}</td>
    `;
    tbody.appendChild(row);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadEmployeeCards();
});

/* Load employees */
function loadEmployeeCards() {
  allEmployees = [
    {
      name: "Amit Sharma",
      calls: 120,
      conversions: 34,
      metrics: {
        "Performance Score": 88,
        "Avg Call Quality": 72,
        "Risk Level": 20,
        "Conversion Rate": 28,
        "Follow-ups Pending": 40,
        "Customer Sentiment": 85
      }
    },
    {
      name: "Neha Verma",
      calls: 95,
      conversions: 22,
      metrics: {
        "Performance Score": 65,
        "Avg Call Quality": 55,
        "Risk Level": 50,
        "Conversion Rate": 23,
        "Follow-ups Pending": 60,
        "Customer Sentiment": 60
      }
    }
  ];

  renderEmployees(allEmployees);
}

/* Render employees */
function renderEmployees(list) {
  const container = document.getElementById("employeeCards");
  container.innerHTML = "";

  if (list.length === 0) {
    container.innerHTML = "<p>No employees found.</p>";
    return;
  }

  list.forEach(emp => {
    const row = document.createElement("div");
    row.className = "employee-row";

    row.innerHTML = `
      <div class="employee-summary">
        <div class="employee-left">
          <div class="employee-icon">👤</div>
          <div>
            <div class="employee-name">${emp.name}</div>
            <div class="employee-basic">
              Calls: ${emp.calls} | Conversions: ${emp.conversions}
            </div>
          </div>
        </div>
      </div>

      <div class="employee-metrics">
        ${renderMetrics(emp.metrics)}
      </div>
    `;

    container.appendChild(row);
  });
}

/* Render metric bars */
function renderMetrics(metrics) {
  return Object.entries(metrics)
    .map(([label, value]) => {
      const color =
        value >= 70 ? "good" :
        value >= 40 ? "ok" :
        "bad";

      return `
        <div class="metric">
          <div class="metric-label">
            <span>${label}</span>
            <span>${value}%</span>
          </div>
          <div class="metric-bar">
            <div class="metric-fill ${color}" style="width:${value}%"></div>
          </div>
        </div>
      `;
    })
    .join("");
}

/* Search filter */
function filterEmployees() {
  const query = document
    .getElementById("employeeSearch")
    .value
    .toLowerCase();

  const filtered = allEmployees.filter(emp =>
    emp.name.toLowerCase().includes(query)
  );

  renderEmployees(filtered);
}