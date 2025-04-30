import { useNavigate } from "react-router-dom";

const AdminMenu = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login-admin");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Panel de Administrador</h1>

      <div
        style={{
          marginTop: "2rem",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <button onClick={() => navigate("/admin/bookings")}>
          Gestión de Reservas
        </button>

        <button onClick={() => navigate("/admin/create-restaurant")}>
          Crear Restaurante
        </button>

        <button onClick={() => navigate("/admin/users")}>
          Gestión de Usuarios
        </button>

        <button onClick={() => navigate("/admin/restaurants")}>
          Gestión de Restaurantes
        </button>

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

export default AdminMenu;
