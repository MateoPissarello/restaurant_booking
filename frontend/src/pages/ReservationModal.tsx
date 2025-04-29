import { useEffect, useState } from "react";

interface Table {
  table_id: number;
  restaurant_id: number;
  number: number;
  capacity: number;
}

interface ReservationModalProps {
  restaurantId: number;
  onClose: () => void;
}

const ReservationModal = ({ restaurantId, onClose }: ReservationModalProps) => {
  const [tables, setTables] = useState<Table[]>([]);
  const [selectedTableId, setSelectedTableId] = useState<number | null>(null);
  const [date, setDate] = useState<string>("");
  const [startTime, setStartTime] = useState<string>("");
  const [endTime, setEndTime] = useState<string>("");
  const [numberOfPeople, setNumberOfPeople] = useState<number>(1);
  const [loading, setLoading] = useState(false);

  const fetchTables = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/table/get_all/${restaurantId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setTables(data);
      } else {
        console.error("Error al obtener mesas");
      }
    } catch (error) {
      console.error("Error en fetchTables", error);
    }
  };

  useEffect(() => {
    fetchTables();
  }, [restaurantId]);

  const handleReserve = async () => {
    if (
      !selectedTableId ||
      !date ||
      !startTime ||
      !endTime ||
      !numberOfPeople
    ) {
      alert("Por favor completa todos los campos.");
      return;
    }

    const body = {
      table_id: selectedTableId,
      restaurant_id: restaurantId,
      date,
      start_time: startTime,
      end_time: endTime,
      number_of_people: numberOfPeople,
    };

    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/booking/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (response.ok) {
        alert("¡Reserva realizada con éxito!");
        onClose();
      } else {
        alert(`Error al reservar: ${data.detail || "Algo salió mal."}`);
      }
    } catch (error) {
      console.error("Error al hacer la reserva", error);
      alert("Ocurrió un error al hacer la reserva.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={modalStyles.overlay}>
      <div style={modalStyles.content}>
        <h2>Hacer una Reserva</h2>

        <div style={{ marginBottom: "1rem" }}>
          <h3>Selecciona una mesa:</h3>
          {tables.length === 0 ? (
            <p>No hay mesas disponibles.</p>
          ) : (
            <ul style={{ maxHeight: "150px", overflowY: "auto" }}>
              {tables.map((table) => (
                <li key={table.table_id} style={{ marginBottom: "0.5rem" }}>
                  <label>
                    <input
                      type="radio"
                      name="selectedTable"
                      value={table.table_id}
                      checked={selectedTableId === table.table_id}
                      onChange={() => setSelectedTableId(table.table_id)}
                    />{" "}
                    Mesa {table.number} (Capacidad: {table.capacity} personas)
                  </label>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Fecha: </label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Hora de inicio: </label>
          <input
            type="time"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Hora de fin: </label>
          <input
            type="time"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            required
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Número de personas: </label>
          <input
            type="number"
            min={1}
            value={numberOfPeople}
            onChange={(e) => setNumberOfPeople(parseInt(e.target.value))}
            required
          />
        </div>

        <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
          <button onClick={handleReserve} disabled={loading}>
            {loading ? "Reservando..." : "Confirmar Reserva"}
          </button>
          <button onClick={onClose}>Cancelar</button>
        </div>
      </div>
    </div>
  );
};

const modalStyles = {
  overlay: {
    position: "fixed" as const,
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "rgba(0,0,0,0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },
  content: {
    backgroundColor: "#fff",
    padding: "2rem",
    borderRadius: "8px",
    maxWidth: "500px",
    width: "100%",
    maxHeight: "90vh",
    overflowY: "auto" as const,
  },
};

export default ReservationModal;
