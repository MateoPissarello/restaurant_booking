import { useEffect, useState } from "react";

interface UserProfile {
  user_id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
}

const MyProfile = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const fetchProfile = async () => {
    try {
      const response = await fetch("http://localhost:8000/users/get/my_info", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        setFormData({
          first_name: data.first_name,
          last_name: data.last_name,
          email: data.email,
          password: "",
        });
      } else {
        alert("Error al obtener la información del perfil.");
      }
    } catch (error) {
      console.error("Error en fetchProfile:", error);
      alert("Error de red.");
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/users/update/my_profile",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            first_name: formData.first_name,
            last_name: formData.last_name,
            email: formData.email,
            password: formData.password || undefined, // No enviar si está vacío
          }),
        }
      );

      if (response.ok) {
        alert("Información actualizada correctamente.");
        fetchProfile();
      } else {
        alert("Error al actualizar la información.");
      }
    } catch (error) {
      console.error("Error en handleUpdate:", error);
      alert("Error al actualizar.");
    }
  };

  if (!profile) return <p>Cargando perfil...</p>;

  return (
    <div style={{ padding: "2rem", maxWidth: "500px", margin: "0 auto" }}>
      <h1>Mi Perfil</h1>

      <label>Nombre:</label>
      <input
        name="first_name"
        value={formData.first_name}
        onChange={handleChange}
        style={{ width: "100%", marginBottom: "1rem" }}
      />

      <label>Apellido:</label>
      <input
        name="last_name"
        value={formData.last_name}
        onChange={handleChange}
        style={{ width: "100%", marginBottom: "1rem" }}
      />

      <label>Email:</label>
      <input
        name="email"
        value={formData.email}
        onChange={handleChange}
        style={{ width: "100%", marginBottom: "1rem" }}
      />

      <label>Contraseña (dejar en blanco si no se cambia):</label>
      <input
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        style={{ width: "100%", marginBottom: "1rem" }}
      />

      <label>Rol (no editable):</label>
      <input
        value={profile.role}
        readOnly
        style={{
          width: "100%",
          marginBottom: "1rem",
          backgroundColor: "#f0f0f0",
        }}
      />

      <button onClick={handleUpdate}>Actualizar</button>
    </div>
  );
};

export default MyProfile;
