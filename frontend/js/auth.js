/* ============================= */
/* API CONFIG (LOCAL + PROD)     */
/* ============================= */

const API =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000/api/auth"
    : "https://salesms-backend.onrender.com/api/auth";
// ⚠️ Make sure this backend URL ACTUALLY works in browser


/* ============================= */
/* MODAL LOGIC                   */
/* ============================= */

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


/* ============================= */
/* SWITCH FORMS                  */
/* ============================= */

function showSignup() {
  signupBox.classList.remove("hidden");
  loginBox.classList.add("hidden");
}

function showLogin() {
  loginBox.classList.remove("hidden");
  signupBox.classList.add("hidden");
}


/* ============================= */
/* SIGNUP                        */
/* ============================= */

async function signupUser() {
  const role = document.getElementById("signupRole").value;
  const email = document.getElementById("signupEmail").value.trim();
  const password = document.getElementById("signupPassword").value.trim();

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

    if (!res.ok) {
      alert(data.message || "Signup failed");
      return;
    }

    alert("Signup successful. Please login.");
    showLogin();

  } catch (err) {
    console.error(err);
    alert("Backend unreachable");
  }
}


/* ============================= */
/* LOGIN                         */
/* ============================= */

async function loginUser() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

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
    console.log("LOGIN RESPONSE:", data);

    if (!res.ok) {
      alert(data.message || "Login failed");
      return;
    }

    // ==============================
    // STORE AUTH DATA
    // ==============================

    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.role);

    const role = data.role?.toLowerCase();

    // ==============================
    // GITHUB PAGES SAFE REDIRECTS
    // (NO LEADING SLASH)
    // ==============================

    if (role === "manager") {
      window.location.href = "manager/dashboard.html";
    } else if (role === "salesperson") {
      window.location.href = "salesperson/dashboard.html";
    } else {
      alert("Invalid role received from server");
      console.error("Invalid role:", data.role);
    }

  } catch (err) {
    console.error(err);
    alert("Backend unreachable");
  }
}
