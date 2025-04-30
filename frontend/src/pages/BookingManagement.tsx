import { useEffect, useState } from "react";
import DeleteConfirmationModal from "./DeleteConfirmationModalAdmin";
import EditBookingModal from "./EditBookingModalAdmin";

interface Booking {
  booking_id: number;
  user_id: number;
  table_id: number;
  restaurant_id: number;
  date: string;
  start_time: string;
  end_time: string;
  number_of_people: number;
  user_info?: {
    first_name: string;
    last_name: string;
    email: string;
  };
}

const BookingManagement = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [selectedBookingForEdit, setSelectedBookingForEdit] =
    useState<Booking | null>(null);
  const [selectedBookingForDelete, setSelectedBookingForDelete] =
    useState<Booking | null>(null);
  const [searchEmail, setSearchEmail] = useState<string>("");

  const fetchAllBookings = async () => {
    try {
      const response = await fetch("http://localhost:8000/booking/get_all", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setBookings(data);
      } else {
        console.error("Error al obtener reservas");
      }
    } catch (error) {
      console.error("Error en fetchAllBookings", error);
    }
  };

  const fetchBookingsByEmail = async () => {
    if (!searchEmail.trim()) return;
    try {
      const response = await fetch(
        `http://localhost:8000/booking/get_by_email/${searchEmail}`,
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
        console.error("Error al buscar reservas por email");
      }
    } catch (error) {
      console.error("Error en fetchBookingsByEmail", error);
    }
  };

  useEffect(() => {
    fetchAllBookings();
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
      <h1>Gestión de Reservas</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="email"
          placeholder="Buscar por email del usuario"
          value={searchEmail}
          onChange={(e) => setSearchEmail(e.target.value)}
          style={{ padding: "0.5rem", marginRight: "0.5rem" }}
        />
        <button onClick={fetchBookingsByEmail}>Buscar</button>
      </div>

      {bookings.length === 0 ? (
        <p>No hay reservas para mostrar.</p>
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
              <p>
                <strong>ID Restaurante:</strong> {booking.restaurant_id}
              </p>
              {booking.user_info && (
                <>
                  <p>
                    <strong>Nombre:</strong> {booking.user_info.first_name}{" "}
                    {booking.user_info.last_name}
                  </p>
                  <p>
                    <strong>Email:</strong> {booking.user_info.email}
                  </p>
                </>
              )}
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

      {selectedBookingForEdit && (
        <EditBookingModal
          booking={selectedBookingForEdit}
          onClose={handleCloseEditModal}
          refreshBookings={fetchAllBookings}
        />
      )}

      {selectedBookingForDelete && (
        <DeleteConfirmationModal
          booking={selectedBookingForDelete}
          onClose={handleCloseDeleteModal}
          refreshBookings={fetchAllBookings}
        />
      )}
    </div>
  );
};

export default BookingManagement;
