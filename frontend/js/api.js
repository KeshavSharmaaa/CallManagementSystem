// ✅ CHANGE THIS TO YOUR REAL BACKEND URL
const API_BASE = "https://backend.onrender.com";

/**
 * Generic API helper
 */
async function apiRequest(endpoint, method = "GET", data = null) {
  const headers = {
    "Content-Type": "application/json"
  };

  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = {
    method,
    headers
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const res = await fetch(API_BASE + endpoint, options);

  // Handle non-JSON or server down
  if (!res.ok) {
    let errorMsg = "API Error";
    try {
      const err = await res.json();
      errorMsg = err.message || errorMsg;
    } catch (_) {}
    throw new Error(errorMsg);
  }

  return res.json();
}
