import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, TOKEN_KEY } from "./api/client";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const login = async () => {
    console.log("1. Login button clicked");

    try {
      setMessage("Connecting to backend...");

      const data = await api.login({
        username,
        password
      });

      console.log("2. Login response received");
      console.log("3. Backend response status:", {
        success: Boolean(data?.access_token),
        user_id: data?.user_id
      });

      if (data?.access_token) {
        console.log("4. Login successful");

        localStorage.setItem(TOKEN_KEY, data.access_token);

        console.log("5. Token saved");

        setMessage("Login successful. Opening dashboard...");

        navigate("/dashboard");
      } else {
        console.log("Login failed");

        setMessage(data?.message || "Invalid username or password");
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