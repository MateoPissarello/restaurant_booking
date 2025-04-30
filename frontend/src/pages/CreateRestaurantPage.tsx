import { useEffect, useState } from "react";

const CreateRestaurantPage = () => {
  const [restaurantData, setRestaurantData] = useState({
    name: "",
    description: "",
    restaurant_type: "",
    phone_number: "",
    address: "",
  });

  const [createdRestaurant, setCreatedRestaurant] = useState<any | null>(null);
  const [schedules, setSchedules] = useState({
    restaurant_id: "",
    day: "Monday",
    opening_hour: "",
    closing_hour: "",
  });

  const [newTable, setNewTable] = useState({
    restaurant_id: "",
    number: 1,
    capacity: 2,
  });
  const [tables, setTables] = useState<{ number: number; capacity: number }[]>(
    []
  );

  const [allRestaurants, setAllRestaurants] = useState<any[]>([]);
  const [successMessage, setSuccessMessage] = useState("");

  const handleCreateRestaurant = async () => {
    try {
      const response = await fetch("http://localhost:8000/restaurant/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(restaurantData),
      });

      if (response.ok) {
        const data = await response.json();
        setCreatedRestaurant(data);
        setSuccessMessage("Restaurante creado correctamente");
        fetchRestaurants();
      } else {
        const error = await response.json();
        alert("Error al crear restaurante: " + error.detail);
      }
    } catch (error) {
      console.error("Error al crear restaurante", error);
    }
  };

  const fetchRestaurants = async () => {
    try {
      const res = await fetch("http://localhost:8000/restaurant/get_all", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setAllRestaurants(data);
      }
    } catch (error) {
      console.error("Error al obtener restaurantes", error);
    }
  };

  const handleCreateSchedule = async () => {
    try {
      const response = await fetch("http://localhost:8000/schedule/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          ...schedules,
          restaurant_id: Number(schedules.restaurant_id),
          day: schedules.day.toLowerCase(), // Conversión a minúsculas
        }),
      });

      if (response.ok) {
        setSuccessMessage("Horario creado correctamente");
      } else {
        const error = await response.json();
        alert("Error al crear horario: " + error.detail);
      }
    } catch (error) {
      console.error("Error al crear horario", error);
    }
  };

  const handleCreateTable = async () => {
    try {
      const response = await fetch("http://localhost:8000/table/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          restaurant_id: Number(newTable.restaurant_id),
          number: newTable.number,
          capacity: newTable.capacity,
        }),
      });

      if (response.ok) {
        setTables([
          ...tables,
          { number: newTable.number, capacity: newTable.capacity },
        ]);
        setSuccessMessage("Mesa creada correctamente");
        setNewTable({ ...newTable, number: newTable.number + 1 });
      } else {
        const error = await response.json();
        alert("Error al crear mesa: " + error.detail);
      }
    } catch (error) {
      console.error("Error al crear mesa", error);
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Crear Restaurante</h1>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          maxWidth: "400px",
        }}
      >
        <label>
          Nombre del restaurante:
          <input
            type="text"
            value={restaurantData.name}
            onChange={(e) =>
              setRestaurantData({ ...restaurantData, name: e.target.value })
            }
          />
        </label>

        <label>
          Descripción:
          <input
            type="text"
            value={restaurantData.description}
            onChange={(e) =>
              setRestaurantData({
                ...restaurantData,
                description: e.target.value,
              })
            }
          />
        </label>

        <label>
          Tipo de restaurante:
          <input
            type="text"
            value={restaurantData.restaurant_type}
            onChange={(e) =>
              setRestaurantData({
                ...restaurantData,
                restaurant_type: e.target.value,
              })
            }
          />
        </label>

        <label>
          Número de teléfono:
          <input
            type="text"
            value={restaurantData.phone_number}
            onChange={(e) =>
              setRestaurantData({
                ...restaurantData,
                phone_number: e.target.value,
              })
            }
          />
        </label>

        <label>
          Dirección:
          <input
            type="text"
            value={restaurantData.address}
            onChange={(e) =>
              setRestaurantData({ ...restaurantData, address: e.target.value })
            }
          />
        </label>

        <button onClick={handleCreateRestaurant}>Crear Restaurante</button>
      </div>

      <hr style={{ margin: "2rem 0" }} />

      <h2>Agregar Horario a Restaurante</h2>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          maxWidth: "400px",
        }}
      >
        <label>
          Restaurante:
          <select
            value={schedules.restaurant_id}
            onChange={(e) =>
              setSchedules({ ...schedules, restaurant_id: e.target.value })
            }
          >
            <option value="">Seleccione un restaurante</option>
            {allRestaurants.map((rest) => (
              <option key={rest.restaurant_id} value={rest.restaurant_id}>
                {rest.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Día de la semana:
          <select
            value={schedules.day}
            onChange={(e) =>
              setSchedules({ ...schedules, day: e.target.value })
            }
          >
            {[
              "Monday",
              "Tuesday",
              "Wednesday",
              "Thursday",
              "Friday",
              "Saturday",
              "Sunday",
            ].map((day) => (
              <option key={day} value={day}>
                {day}
              </option>
            ))}
          </select>
        </label>

        <label>
          Hora de apertura:
          <input
            type="time"
            value={schedules.opening_hour}
            onChange={(e) =>
              setSchedules({ ...schedules, opening_hour: e.target.value })
            }
          />
        </label>

        <label>
          Hora de cierre:
          <input
            type="time"
            value={schedules.closing_hour}
            onChange={(e) =>
              setSchedules({ ...schedules, closing_hour: e.target.value })
            }
          />
        </label>

        <button onClick={handleCreateSchedule}>Agregar Horario</button>
      </div>

      <hr style={{ margin: "2rem 0" }} />

      <h2>Agregar Mesa a Restaurante</h2>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          maxWidth: "400px",
        }}
      >
        <label>
          Restaurante:
          <select
            value={newTable.restaurant_id}
            onChange={(e) =>
              setNewTable({ ...newTable, restaurant_id: e.target.value })
            }
          >
            <option value="">Seleccione un restaurante</option>
            {allRestaurants.map((rest) => (
              <option key={rest.restaurant_id} value={rest.restaurant_id}>
                {rest.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Número de mesa:
          <input
            type="number"
            value={newTable.number}
            onChange={(e) =>
              setNewTable({ ...newTable, number: Number(e.target.value) })
            }
          />
        </label>

        <label>
          Capacidad de la mesa:
          <input
            type="number"
            value={newTable.capacity}
            onChange={(e) =>
              setNewTable({ ...newTable, capacity: Number(e.target.value) })
            }
          />
        </label>

        <button onClick={handleCreateTable}>Agregar Mesa</button>

        <ul>
          {tables.map((table, idx) => (
            <li key={idx}>
              Mesa #{table.number} - Capacidad: {table.capacity}
            </li>
          ))}
        </ul>
      </div>

      {successMessage && (
        <p style={{ color: "green", marginTop: "1rem" }}>{successMessage}</p>
      )}
    </div>
  );
};

export default CreateRestaurantPage;
