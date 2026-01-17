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
      ? "/api/auth/register/manager"
      : "/api/auth/register/salesperson";

  try {
    const data = await apiRequest(endpoint, "POST", { email, password });
    alert(data.message || "Signup successful");
    showLogin();
  } catch (err) {
    alert(err.message || "Signup failed");
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
    const data = await apiRequest("/api/auth/login", "POST", {
      email,
      password
    });

    console.log("LOGIN RESPONSE:", data);

    // ✅ STORE AUTH INFO
    if (data.token) localStorage.setItem("token", data.token);
    if (data.role) localStorage.setItem("role", data.role);

    const role = data.role?.toLowerCase();

    if (role === "manager") {
      window.location.href = "/manager/dashboard.html";
    } else if (role === "salesperson") {
      window.location.href = "/salesperson/dashboard.html";
    } else {
      alert("Invalid role received");
    }
  } catch (err) {
    alert("Backend unreachable");
    console.error(err);
  }
}
