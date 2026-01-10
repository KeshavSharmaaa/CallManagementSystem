const API_BASE = "http://127.0.0.1:5000/api";

async function apiRequest(endpoint, method = "GET", data = null) {
  const headers = { "Content-Type": "application/json" };

  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = { method, headers };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(API_BASE + endpoint, options);
  return response.json();
}
