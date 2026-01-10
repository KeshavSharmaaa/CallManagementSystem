let callSid = null;
let timerInterval = null;
let secondsElapsed = 0;
let callEnded = false;

/* ---------------- AUTH GUARD ---------------- */
if (!localStorage.getItem("token")) {
  window.location.href = "/";
}

/* ---------------- TIMER ---------------- */
function startTimer() {
  timerInterval = setInterval(() => {
    secondsElapsed++;
    const min = String(Math.floor(secondsElapsed / 60)).padStart(2, "0");
    const sec = String(secondsElapsed % 60).padStart(2, "0");
    document.getElementById("timer").innerText = `${min}:${sec}`;
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
}

/* ---------------- START CALL ---------------- */
async function startCall() {
  const agentPhone = "+91XXXXXXXXXX"; // 🔴 replace
  const customerPhone = "+91XXXXXXXXXX"; // 🔴 replace
  const salespersonId = localStorage.getItem("userId");

  const res = await fetch("/api/call/dial", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({
      agentPhone,
      customerPhone,
      salespersonId
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.message || "Failed to start call");
    return;
  }

  callSid = data.callSid;
  secondsElapsed = 0;
  startTimer();

  document.getElementById("startCallBtn").disabled = true;
  document.getElementById("endCallBtn").disabled = false;
}

/* ---------------- END CALL ---------------- */
async function endCall() {
  stopTimer();

  const outcome = document.getElementById("outcome").value;

  await fetch("/api/call/end", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({
      callSid,
      duration: secondsElapsed,
      outcome
    })
  });

  callEnded = true;

  alert("Call ended. Please upload and submit the recording.");

  // Enable submit ONLY if file already selected
  const audioFile = document.getElementById("audioFile").files[0];
  if (audioFile) {
    document.getElementById("submitRecordingBtn").disabled = false;
  }

  document.getElementById("endCallBtn").disabled = true;
}

function onRecordingSelected() {
  const fileSelected = document.getElementById("audioFile").files.length > 0;

  if (fileSelected) {
    document.getElementById("submitRecordingBtn").disabled = false;
  }
}

async function submitRecording() {
  const submitBtn = document.getElementById("submitRecordingBtn");
  const audioFile = document.getElementById("audioFile").files[0];
  const outcome = document.getElementById("outcome").value;

  if (!audioFile) {
    alert("Please select a recording file first");
    return;
  }

  // 🔒 HARD LOCK
  submitBtn.disabled = true;
  submitBtn.innerText = "Uploading...";

  await uploadRecording(audioFile, outcome);

  submitBtn.innerText = "Uploaded";
}

/* ---------------- UPLOAD RECORDING ---------------- */
async function uploadRecording(file, outcome) {
  const formData = new FormData();
  formData.append("audio", file);
  formData.append("salespersonId", localStorage.getItem("userId"));
  formData.append("outcome", outcome);

  const res = await fetch("/api/call/upload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: formData
  });

  const data = await res.json();
  console.log("Upload result:", data);

  if (!res.ok || !data.success) {
    alert("Failed to process call recording");
    return;
  }

  // 🔥 SHOW RESULTS ON UI
  renderResults(data);
}

function renderResults(data) {
  const resultsDiv = document.getElementById("callResults");
  const transcriptEl = document.getElementById("transcriptText");
  const analysisList = document.getElementById("analysisList");

  resultsDiv.style.display = "block";

  // Transcript
  transcriptEl.innerText = data.transcript || "No transcript available";

  // Analysis
  analysisList.innerHTML = "";

  const analysis = data.analysis || {};

  Object.entries(analysis).forEach(([key, value]) => {
    const li = document.createElement("li");

    if (typeof value === "object") {
      li.innerHTML = `<strong>${key.replace("_", " ")}:</strong> ${JSON.stringify(value)}`;
    } else {
      li.innerHTML = `<strong>${key.replace("_", " ")}:</strong> ${value}`;
    }
  
    analysisList.appendChild(li);
  });


  // Scroll into view
  resultsDiv.scrollIntoView({ behavior: "smooth" });
}

/* ---------------- INIT ---------------- */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("startCallBtn")
    ?.addEventListener("click", startCall);

  document.getElementById("endCallBtn")
    ?.addEventListener("click", endCall);

  document.getElementById("submitRecordingBtn")
    ?.addEventListener("click", submitRecording);

  document.getElementById("audioFile")
    ?.addEventListener("change", onRecordingSelected);
});