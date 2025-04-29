import { useEffect, useState } from "react";
import DeleteConfirmationModal from "./DeleteConfirmationModal";
import EditBookingModal from "./EditBookingModal";
// import DeleteConfirmationModal from "./DeleteConfirmationModal"; // Este todavía lo vamos a crear

interface Booking {
  booking_id: number;
  user_id: number;
  table_id: number;
  restaurant_id: number;
  date: string;
  start_time: string;
  end_time: string;
  number_of_people: number;
}

const MyBookings = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [selectedBookingForEdit, setSelectedBookingForEdit] =
    useState<Booking | null>(null);
  const [selectedBookingForDelete, setSelectedBookingForDelete] =
    useState<Booking | null>(null);

  const fetchBookings = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/booking/get/my_bookings",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setBookings(data);
      } else {
        console.error("Error al obtener reservas");
      }
    } catch (error) {
      console.error("Error en fetchBookings", error);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleOpenEditModal = (booking: Booking) => {
    setSelectedBookingForEdit(booking);
  };

  const handleCloseEditModal = () => {
    setSelectedBookingForEdit(null);
  };

  const handleOpenDeleteModal = (booking: Booking) => {
    setSelectedBookingForDelete(booking);
  };

  const handleCloseDeleteModal = () => {
    setSelectedBookingForDelete(null);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Mis Reservas</h1>

      {bookings.length === 0 ? (
        <p>No tienes reservas actualmente.</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
            gap: "1rem",
            marginTop: "2rem",
          }}
        >
          {bookings.map((booking) => (
            <div
              key={booking.booking_id}
              style={{
                border: "1px solid gray",
                padding: "1rem",
                borderRadius: "8px",
              }}
            >
              <p>
                <strong>Fecha:</strong> {booking.date}
              </p>
              <p>
                <strong>Hora Inicio:</strong> {booking.start_time}
              </p>
              <p>
                <strong>Hora Fin:</strong> {booking.end_time}
              </p>
              <p>
                <strong>Número de Personas:</strong> {booking.number_of_people}
              </p>
              <p>
                <strong>ID Mesa:</strong> {booking.table_id}
              </p>

              <div
                style={{ marginTop: "1rem", display: "flex", gap: "0.5rem" }}
              >
                <button onClick={() => handleOpenEditModal(booking)}>
                  Modificar
                </button>

                <button
                  onClick={() => handleOpenDeleteModal(booking)}
                  style={{ backgroundColor: "red", color: "white" }}
                >
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal para Editar Reserva */}
      {selectedBookingForEdit && (
        <EditBookingModal
          booking={selectedBookingForEdit}
          onClose={handleCloseEditModal}
          onUpdate={fetchBookings} // Este es el prop correcto
        />
      )}

      {selectedBookingForDelete && (
        <DeleteConfirmationModal
          booking={selectedBookingForDelete}
          onClose={handleCloseDeleteModal}
          onUpdate={fetchBookings}
        />
      )}
    </div>
  );
};

export default MyBookings;
