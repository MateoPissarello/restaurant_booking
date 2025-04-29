import { useEffect, useState } from "react";

interface Table {
  table_id: number;
  number: number;
  capacity: number;
}

interface Booking {
  booking_id: number;
  restaurant_id: number;
  table_id: number;
  date: string;
  start_time: string;
  end_time: string;
  number_of_people: number;
}

interface EditBookingModalProps {
  booking: Booking;
  onClose: () => void;
  onUpdate: () => void; // para recargar después de actualizar
}

const EditBookingModal = ({
  booking,
  onClose,
  onUpdate,
}: EditBookingModalProps) => {
  const [tables, setTables] = useState<Table[]>([]);
  const [selectedTableId, setSelectedTableId] = useState<number | undefined>(
    booking.table_id
  );
  const [date, setDate] = useState<string>(booking.date);
  const [startTime, setStartTime] = useState<string>(booking.start_time);
  const [endTime, setEndTime] = useState<string>(booking.end_time);
  const [numberOfPeople, setNumberOfPeople] = useState<number>(
    booking.number_of_people
  );

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/table/get_all/${booking.restaurant_id}`,
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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const updatedFields: any = {};

    if (selectedTableId !== booking.table_id)
      updatedFields.table_id = selectedTableId;
    if (date !== booking.date) updatedFields.date = date;
    if (startTime !== booking.start_time) updatedFields.start_time = startTime;
    if (endTime !== booking.end_time) updatedFields.end_time = endTime;
    if (numberOfPeople !== booking.number_of_people)
      updatedFields.number_of_people = numberOfPeople;

    if (Object.keys(updatedFields).length === 0) {
      alert("No has cambiado ningún campo.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/booking/update/${booking.booking_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(updatedFields),
        }
      );

      if (response.ok) {
        alert("Reserva actualizada exitosamente");
        onUpdate(); // Recargar la lista
        onClose();
      } else {
        console.error("Error al actualizar reserva");
        alert("Error al actualizar reserva");
      }
    } catch (error) {
      console.error("Error en actualización de reserva", error);
    }
  };

  return (
    <div style={modalStyle}>
      <h2>Editar Reserva</h2>
      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
      >
        <div>
          <label>Mesa:</label>
          <select
            value={selectedTableId}
            onChange={(e) => setSelectedTableId(Number(e.target.value))}
          >
            {tables.map((table) => (
              <option key={table.table_id} value={table.table_id}>
                Mesa {table.number} - Capacidad {table.capacity}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Fecha:</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div>
          <label>Hora de Inicio:</label>
          <input
            type="time"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
        </div>

        <div>
          <label>Hora de Fin:</label>
          <input
            type="time"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
        </div>

        <div>
          <label>Número de Personas:</label>
          <input
            type="number"
            value={numberOfPeople}
            onChange={(e) => setNumberOfPeople(Number(e.target.value))}
          />
        </div>

        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <button type="submit">Guardar Cambios</button>
          <button
            type="button"
            onClick={onClose}
            style={{ backgroundColor: "red", color: "white" }}
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

const modalStyle: React.CSSProperties = {
  position: "fixed",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  background: "white",
  padding: "2rem",
  borderRadius: "8px",
  zIndex: 1000,
  width: "90%",
  maxWidth: "500px",
};

export default EditBookingModal;
