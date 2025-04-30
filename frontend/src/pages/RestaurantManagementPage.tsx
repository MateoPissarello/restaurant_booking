import { useEffect, useState } from "react";

const RestaurantManagementPage = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [schedules, setSchedules] = useState({});
  const [tables, setTables] = useState({});
  const [editingRestaurant, setEditingRestaurant] = useState(null);
  const [editFormData, setEditFormData] = useState({});
  const [scheduleModalRestaurantId, setScheduleModalRestaurantId] =
    useState(null);
  const [tableModalRestaurantId, setTableModalRestaurantId] = useState(null);
  const [newSchedule, setNewSchedule] = useState({
    day: "",
    opening_hour: "",
    closing_hour: "",
  });
  const [newTable, setNewTable] = useState({
    number: "",
    capacity: "",
  });

  const fetchRestaurants = async () => {
    try {
      const res = await fetch("http://localhost:8000/restaurant/get_all", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const data = await res.json();
      setRestaurants(data);
      for (const r of data) {
        fetchSchedules(r.restaurant_id);
        fetchTables(r.restaurant_id);
      }
    } catch (e) {
      console.error("Error fetching restaurants", e);
    }
  };

  const fetchSchedules = async (restaurant_id) => {
    try {
      const res = await fetch(
        `http://localhost:8000/schedule/get/${restaurant_id}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      const data = await res.json();
      setSchedules((prev) => ({
        ...prev,
        [restaurant_id]: Array.isArray(data) ? data : [],
      }));
    } catch (e) {
      console.error("Error fetching schedules", e);
    }
  };

  const fetchTables = async (restaurant_id) => {
    try {
      const res = await fetch(
        `http://localhost:8000/table/get_all/${restaurant_id}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      const data = await res.json();
      setTables((prev) => ({ ...prev, [restaurant_id]: data }));
    } catch (e) {
      console.error("Error fetching tables", e);
    }
  };

  const handleEditClick = (restaurant) => {
    setEditingRestaurant(restaurant.restaurant_id);
    setEditFormData({ ...restaurant });
  };

  const handleUpdateRestaurant = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/restaurant/update/${editingRestaurant}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(editFormData),
        }
      );
      if (res.ok) {
        setEditingRestaurant(null);
        fetchRestaurants();
      } else {
        const err = await res.json();
        alert("Error: " + err.detail);
      }
    } catch (e) {
      console.error("Error updating restaurant", e);
    }
  };

  const handleDeleteSchedule = async (schedule_id) => {
    if (!confirm("¿Eliminar horario?")) return;
    try {
      const res = await fetch(
        `http://localhost:8000/schedule/delete/${schedule_id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (res.ok) {
        fetchRestaurants();
      } else {
        const err = await res.json();
        alert("Error: " + err.detail);
      }
    } catch (e) {
      console.error("Error deleting schedule", e);
    }
  };

  const handleOpenScheduleModal = (restaurant_id) => {
    setNewSchedule({ day: "", opening_hour: "", closing_hour: "" });
    setScheduleModalRestaurantId(restaurant_id);
  };

  const handleCreateSchedule = async () => {
    try {
      const res = await fetch("http://localhost:8000/schedule/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          ...newSchedule,
          restaurant_id: scheduleModalRestaurantId,
        }),
      });
      if (res.ok) {
        fetchSchedules(scheduleModalRestaurantId);
        setScheduleModalRestaurantId(null);
      } else {
        const err = await res.json();
        alert("Error: " + err.detail);
      }
    } catch (e) {
      console.error("Error creating schedule", e);
    }
  };

  const handleUpdateTable = async (table_id, update) => {
    try {
      const res = await fetch(
        `http://localhost:8000/table/update/${table_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(update),
        }
      );
      if (res.ok) {
        fetchRestaurants();
      } else {
        const err = await res.json();
        alert("Error: " + err.detail);
      }
    } catch (e) {
      console.error("Error updating table", e);
    }
  };

  const handleOpenTableModal = (restaurant_id) => {
    setNewTable({ number: "", capacity: "" });
    setTableModalRestaurantId(restaurant_id);
  };

  const handleCreateTable = async () => {
    try {
      const res = await fetch("http://localhost:8000/table/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          ...newTable,
          restaurant_id: tableModalRestaurantId,
        }),
      });
      if (res.ok) {
        fetchTables(tableModalRestaurantId);
        setTableModalRestaurantId(null);
      } else {
        const err = await res.json();
        alert("Error: " + err.detail);
      }
    } catch (e) {
      console.error("Error creating table", e);
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Gestión de Restaurantes</h1>
      {restaurants.map((r) => (
        <div
          key={r.restaurant_id}
          style={{
            border: "1px solid #ccc",
            padding: "1rem",
            marginBottom: "1rem",
          }}
        >
          {editingRestaurant === r.restaurant_id ? (
            <div>
              <input
                placeholder="Nombre"
                value={editFormData.name || ""}
                onChange={(e) =>
                  setEditFormData({ ...editFormData, name: e.target.value })
                }
              />
              <input
                placeholder="Descripción"
                value={editFormData.description || ""}
                onChange={(e) =>
                  setEditFormData({
                    ...editFormData,
                    description: e.target.value,
                  })
                }
              />
              <input
                placeholder="Tipo"
                value={editFormData.restaurant_type || ""}
                onChange={(e) =>
                  setEditFormData({
                    ...editFormData,
                    restaurant_type: e.target.value,
                  })
                }
              />
              <input
                placeholder="Teléfono"
                value={editFormData.phone_number || ""}
                onChange={(e) =>
                  setEditFormData({
                    ...editFormData,
                    phone_number: e.target.value,
                  })
                }
              />
              <input
                placeholder="Dirección"
                value={editFormData.address || ""}
                onChange={(e) =>
                  setEditFormData({ ...editFormData, address: e.target.value })
                }
              />
              <button onClick={handleUpdateRestaurant}>Guardar</button>
              <button onClick={() => setEditingRestaurant(null)}>
                Cancelar
              </button>
            </div>
          ) : (
            <div>
              <h3>{r.name}</h3>
              <p>{r.description}</p>
              <p>Tipo: {r.restaurant_type}</p>
              <p>Tel: {r.phone_number}</p>
              <p>Dirección: {r.address}</p>
              <button onClick={() => handleEditClick(r)}>Editar</button>
            </div>
          )}

          <h4>Horarios</h4>
          <ul>
            {(schedules[r.restaurant_id] || []).map((s) => (
              <li key={s.schedule_id}>
                {s.day}: {s.opening_hour} - {s.closing_hour}
                <button onClick={() => handleDeleteSchedule(s.schedule_id)}>
                  Eliminar
                </button>
              </li>
            ))}
          </ul>
          <button onClick={() => handleOpenScheduleModal(r.restaurant_id)}>
            Añadir Horario
          </button>

          <h4>Mesas</h4>
          <ul>
            {(tables[r.restaurant_id] || []).map((t) => (
              <li key={t.table_id}>
                Mesa #{t.number} - Capacidad: {t.capacity}
                <button
                  onClick={() =>
                    handleUpdateTable(t.table_id, {
                      number: prompt("Nuevo número", t.number),
                      capacity: prompt("Nueva capacidad", t.capacity),
                    })
                  }
                >
                  Editar
                </button>
              </li>
            ))}
          </ul>
          <button onClick={() => handleOpenTableModal(r.restaurant_id)}>
            Añadir Mesa
          </button>
        </div>
      ))}

      {scheduleModalRestaurantId && (
        <div className="modal">
          <div className="modal-content">
            <h3>Añadir Horario</h3>
            <input
              placeholder="Día (ej. monday)"
              value={newSchedule.day}
              onChange={(e) =>
                setNewSchedule({ ...newSchedule, day: e.target.value })
              }
            />
            <input
              placeholder="Hora de apertura (HH:MM)"
              value={newSchedule.opening_hour}
              onChange={(e) =>
                setNewSchedule({ ...newSchedule, opening_hour: e.target.value })
              }
            />
            <input
              placeholder="Hora de cierre (HH:MM)"
              value={newSchedule.closing_hour}
              onChange={(e) =>
                setNewSchedule({ ...newSchedule, closing_hour: e.target.value })
              }
            />
            <br />
            <button onClick={handleCreateSchedule}>Guardar</button>
            <button onClick={() => setScheduleModalRestaurantId(null)}>
              Cancelar
            </button>
          </div>
        </div>
      )}

      {tableModalRestaurantId && (
        <div className="modal">
          <div className="modal-content">
            <h3>Añadir Mesa</h3>
            <input
              placeholder="Número de mesa"
              value={newTable.number}
              onChange={(e) =>
                setNewTable({ ...newTable, number: e.target.value })
              }
            />
            <input
              placeholder="Capacidad"
              value={newTable.capacity}
              onChange={(e) =>
                setNewTable({ ...newTable, capacity: e.target.value })
              }
            />
            <br />
            <button onClick={handleCreateTable}>Guardar</button>
            <button onClick={() => setTableModalRestaurantId(null)}>
              Cancelar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RestaurantManagementPage;
