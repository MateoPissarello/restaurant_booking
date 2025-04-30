import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginAdmin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const response = await fetch("http://localhost:8000/auth/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        navigate("/admin-menu");
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Error de autenticación");
      }
    } catch (error) {
      console.error("Error en login:", error);
      setErrorMessage("Error de conexión");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Login Administrador</h1>
      <form
        onSubmit={handleLogin}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          maxWidth: "400px",
        }}
      >
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {errorMessage && (
          <div
            style={{
              backgroundColor: "#ffe0e0",
              color: "#d00000",
              padding: "1rem",
              borderRadius: "8px",
              border: "1px solid #d00000",
              fontSize: "0.9rem",
            }}
          >
            <strong>Error:</strong> {errorMessage}
          </div>
        )}

        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
};

export default LoginAdmin;
