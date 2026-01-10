async function loadInsights() {
  try {
    const res = await fetch("/api/manager/call-insights", {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    });

    const data = await res.json();
    const tbody = document.querySelector("#insightsTable tbody");
    tbody.innerHTML = "";

    if (!data.success || !data.data.length) {
      tbody.innerHTML = "<tr><td colspan='10'>No insights found</td></tr>";
      return;
    }

    data.data.forEach(call => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${call.salespersonId || "-"}</td>
        <td>${call.duration}s</td>
        <td>${call.outcome}</td>

        ${metricCell(call.analysis.engagement)}
        ${metricCell(call.analysis.consistency)}
        ${metricCell(call.analysis.effectiveness)}

        <td>
          <div class="score">${call.analysis.risk.level}</div>
          <div class="explain">${call.analysis.risk.explanation}</div>
        </td>

        <td style="max-width:220px">${call.transcript || "-"}</td>

        <td>
          <audio controls src="/uploads/calls/${fileName(call.audioFilePath)}"></audio>
        </td>

        <td>${new Date(call.createdAt).toLocaleString()}</td>
      `;

      tbody.appendChild(tr);
    });

  } catch (err) {
    console.error(err);
    alert("Unable to load insights");
  }
}

function metricCell(metric) {
  if (!metric) return "<td>-</td>";
  return `
    <td>
      <div class="score">${metric.score}</div>
      <div class="explain">${metric.explanation}</div>
    </td>
  `;
}

function fileName(path) {
  return path.split("\\").pop().split("/").pop();
}

document.addEventListener("DOMContentLoaded", loadInsights);
