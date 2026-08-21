import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const login = async () => {
    const response = await fetch("http://127.0.0.1:8000/users/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });

    const data = await response.json();

    if (response.ok && data.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", data.username);
      localStorage.setItem("role", data.role);

      navigate("/dashboard");
    } else {
      alert("Invalid username or password");
    }
  };

  return (
    <div>
      <h1>Spotify Tech</h1>

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>
    </div>
  );
}

export default Login;