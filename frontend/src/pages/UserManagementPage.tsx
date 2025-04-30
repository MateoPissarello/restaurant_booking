import { useEffect, useState } from "react";

const UserManagementPage = () => {
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [editFormData, setEditFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    role: "",
  });

  const [newUserData, setNewUserData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    role: "",
  });

  const fetchUsers = async () => {
    try {
      const response = await fetch("http://localhost:8000/users/get_all", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else {
        console.error("Error al obtener usuarios");
      }
    } catch (error) {
      console.error("Error al obtener usuarios", error);
    }
  };

  const handleEditClick = (user) => {
    setEditingUser(user);
    setEditFormData({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      password: "", // no debe cargar la contraseña
      role: user.role,
    });
  };

  const handleUpdateUser = async () => {
    try {
      const cleanedData = { ...editFormData };
      if (!cleanedData.password) {
        delete cleanedData.password; // Evitar enviar password vacío
      }

      console.log("Actualizando usuario:", cleanedData); // Log para depurar

      const response = await fetch(
        `http://localhost:8000/users/update/user/${editingUser.user_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(cleanedData),
        }
      );

      if (response.ok) {
        setEditingUser(null);
        fetchUsers();
        alert("Usuario actualizado exitosamente");
      } else {
        const error = await response.json();
        alert("Error al actualizar usuario: " + error.detail);
      }
    } catch (error) {
      console.error("Error al actualizar usuario", error);
    }
  };

  const handleDeleteUser = async (user_id) => {
    if (!confirm("¿Seguro que deseas eliminar este usuario?")) return;

    try {
      const response = await fetch(
        `http://localhost:8000/users/delete/user/${user_id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (response.ok) {
        fetchUsers();
      } else {
        const error = await response.json();
        alert("Error al eliminar usuario: " + error.detail);
      }
    } catch (error) {
      console.error("Error al eliminar usuario", error);
    }
  };

  const handleCreateUser = async () => {
    try {
      // Verificación previa
      if (
        !newUserData.first_name ||
        !newUserData.last_name ||
        !newUserData.email ||
        !newUserData.password ||
        !newUserData.role
      ) {
        alert("Por favor, completa todos los campos.");
        return;
      }

      console.log("Creando nuevo usuario:", newUserData); // Log para depura

      const response = await fetch("http://localhost:8000/users/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(newUserData),
      });

      if (response.ok) {
        setNewUserData({
          first_name: "",
          last_name: "",
          email: "",
          password: "",
          role: "",
        });
        fetchUsers();
        alert("Usuario creado exitosamente");
      } else {
        const error = await response.json();
        alert("Error al crear usuario: " + error.detail);
      }
    } catch (error) {
      console.error("Error al crear usuario", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Gestión de Usuarios</h1>

      {/* Formulario para crear nuevo usuario */}
      <div
        style={{ marginTop: "2rem", border: "1px solid #ccc", padding: "1rem" }}
      >
        <h2>Crear Nuevo Usuario</h2>
        <input
          type="text"
          placeholder="Nombre"
          value={newUserData.first_name}
          onChange={(e) =>
            setNewUserData({ ...newUserData, first_name: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Apellido"
          value={newUserData.last_name}
          onChange={(e) =>
            setNewUserData({ ...newUserData, last_name: e.target.value })
          }
        />
        <input
          type="email"
          placeholder="Email"
          value={newUserData.email}
          onChange={(e) =>
            setNewUserData({ ...newUserData, email: e.target.value })
          }
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={newUserData.password}
          onChange={(e) =>
            setNewUserData({ ...newUserData, password: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Rol"
          value={newUserData.role}
          onChange={(e) =>
            setNewUserData({ ...newUserData, role: e.target.value })
          }
        />
        <button onClick={handleCreateUser}>Crear Usuario</button>
      </div>

      {/* Tabla de usuarios */}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.user_id}>
              <td>{user.first_name}</td>
              <td>{user.last_name}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>
                <button onClick={() => handleEditClick(user)}>Editar</button>
                <button
                  onClick={() => handleDeleteUser(user.user_id)}
                  style={{ marginLeft: "0.5rem" }}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal de edición de usuario */}
      {editingUser && (
        <div
          style={{
            marginTop: "2rem",
            border: "1px solid #ccc",
            padding: "1rem",
          }}
        >
          <h2>Editar Usuario</h2>
          <input
            type="text"
            placeholder="Nombre"
            value={editFormData.first_name}
            onChange={(e) =>
              setEditFormData({ ...editFormData, first_name: e.target.value })
            }
          />
          <input
            type="text"
            placeholder="Apellido"
            value={editFormData.last_name}
            onChange={(e) =>
              setEditFormData({ ...editFormData, last_name: e.target.value })
            }
          />
          <input
            type="email"
            placeholder="Email"
            value={editFormData.email}
            onChange={(e) =>
              setEditFormData({ ...editFormData, email: e.target.value })
            }
          />
          <input
            type="password"
            placeholder="Nueva contraseña (opcional)"
            value={editFormData.password}
            onChange={(e) =>
              setEditFormData({ ...editFormData, password: e.target.value })
            }
          />
          <input
            type="text"
            placeholder="Rol"
            value={editFormData.role}
            onChange={(e) =>
              setEditFormData({ ...editFormData, role: e.target.value })
            }
          />
          <button onClick={handleUpdateUser}>Guardar cambios</button>
          <button
            onClick={() => setEditingUser(null)}
            style={{ marginLeft: "0.5rem" }}
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  );
};

export default UserManagementPage;
