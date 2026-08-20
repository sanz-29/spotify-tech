import { useState } from "react";
import axios from "axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const login = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/users/login",
        {
          username: username,
          password: password
        }
      );

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      setMessage("Login successful");
    } catch (error) {
      setMessage("Invalid username or password");
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

      <br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />

      <button onClick={login}>
        Login
      </button>

      <p>{message}</p>
    </div>
  );
}

export default Login;