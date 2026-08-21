import { useEffect, useState } from "react";

function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/";
      return;
    }

    fetch("http://127.0.0.1:8000/users/me", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unauthorized");
        }

        return response.json();
      })
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        localStorage.removeItem("token");
        window.location.href = "/";
      });
  }, []);

  if (!user) {
    return <h2>Loading...</h2>;
  }

  return (
    <div>
      <h1>Spotify Tech</h1>

      <h2>Dashboard</h2>

      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
      <p>Role: {user.role}</p>

      <button
        onClick={() => {
          localStorage.removeItem("token");
          window.location.href = "/";
        }}
      >
        Logout
      </button>
    </div>
  );
}

export default Dashboard;