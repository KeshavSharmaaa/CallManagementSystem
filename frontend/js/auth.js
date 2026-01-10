const API = "/api/auth";

// ---------- MODAL LOGIC ----------
const modal = document.getElementById("authModal");
const signupBox = document.getElementById("signupBox");
const loginBox = document.getElementById("loginBox");

function openLogin() {
  modal.classList.add("active");
  showLogin();
}

function openSignup() {
  modal.classList.add("active");
  showSignup();
}

function closeAuth() {
  modal.classList.remove("active");
}

// ---------- SWITCH FORMS ----------
function showSignup() {
  signupBox.classList.remove("hidden");
  loginBox.classList.add("hidden");
}

function showLogin() {
  loginBox.classList.remove("hidden");
  signupBox.classList.add("hidden");
}

// ---------- SIGNUP ----------
async function signupUser() {
  const role = document.getElementById("signupRole").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;

  if (!email || !password) {
    alert("Please fill all fields");
    return;
  }

  const endpoint =
    role === "manager"
      ? "/register/manager"
      : "/register/salesperson";

  try {
    const res = await fetch(API + endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    alert(data.message || "Signup successful");

    if (res.ok) showLogin();
  } catch (err) {
    alert("Server error. Please try again.");
  }
}

// ---------- LOGIN ----------
async function loginUser() {
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  if (!email || !password) {
    alert("Please fill all fields");
    return;
  }

  try {
    const res = await fetch(API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log("LOGIN RESPONSE:", data); // 🔍 DEBUG

    if (!res.ok) {
      alert(data.message || "Login failed");
      return;
    }

    // ✅ STORE AUTH INFO
    if (data.token) localStorage.setItem("token", data.token);
    if (data.role) localStorage.setItem("role", data.role);

    // ✅ NORMALIZE ROLE
    const role = data.role?.toLowerCase();

    if (role === "manager") {
      window.location.href = "/manager/dashboard.html";
    } else if (role === "salesperson") {
      window.location.href = "/salesperson/dashboard.html";
    } else {
      alert("Login successful but role missing or invalid");
      console.error("Invalid role:", data.role);
    }

  } catch (err) {
    alert("Unable to connect to server");
  }
}
