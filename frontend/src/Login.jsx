import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("sanjay");
  const [password, setPassword] = useState("mypassword");
  const [message, setMessage] = useState("");

  const login = async () => {
    console.log("1. Login button clicked");

    try {
      setMessage("Connecting to backend...");

      const response = await fetch(
        "http://127.0.0.1:8000/users/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify({
            username: username,
            password: password
          })
        }
      );

      console.log("2. Backend response status:", response.status);

      const data = await response.json();

      console.log("3. Backend response data:", data);

      if (response.ok && data.access_token) {
        console.log("4. Login successful");

        localStorage.setItem("token", data.access_token);

        console.log("5. Token saved");

        setMessage("Login successful. Opening dashboard...");

        navigate("/dashboard");
      } else {
        console.log("Login failed");

        setMessage(data.message || "Invalid username or password");
      }

    } catch (error) {
      console.error("LOGIN ERROR:", error);

      setMessage("Backend connection failed");
    }
  };

  return (
    <div>
      <h1>Spotify Tech</h1>

      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <br />
      <br />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />
      <br />

      <button onClick={login}>
        Login
      </button>

      <p>{message}</p>
    </div>
  );
}

export default Login;