import { useNavigate } from "react-router-dom";

const MainMenu = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login-client");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Menú Principal Cliente</h1>
      <div
        style={{
          marginTop: "2rem",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <button onClick={() => navigate("/make-reservation")}>
          Hacer una Reserva
        </button>

        <button onClick={() => navigate("/my-reservations")}>
          Ver Mis Reservas
        </button>

        <button onClick={() => navigate("/my-profile")}>Ver Mi Perfil</button>

        <button
          onClick={handleLogout}
          style={{ marginTop: "2rem", color: "red" }}
        >
          Cerrar Sesión
        </button>
      </div>
    </div>
  );
};

export default MainMenu;
