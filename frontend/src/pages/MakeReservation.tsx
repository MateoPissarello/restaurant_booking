import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ReservationModal from "./ReservationModal"; // Nuevo modal de reservas
import ScheduleModal from "./ScheduleModal"; // Asegúrate que la ruta esté correcta

interface Restaurant {
  restaurant_id: number;
  name: string;
  description: string;
  restaurant_type: string;
  phone_number: string;
  address: string;
}

const MakeReservation = () => {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [selectedRestaurantIdForSchedule, setSelectedRestaurantIdForSchedule] =
    useState<number | null>(null);
  const [
    selectedRestaurantIdForReservation,
    setSelectedRestaurantIdForReservation,
  ] = useState<number | null>(null);

  const fetchRestaurants = async () => {
    try {
      const response = await fetch("http://localhost:8000/restaurant/get_all", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setRestaurants(data);
      } else {
        console.error("Error al obtener restaurantes");
      }
    } catch (error) {
      console.error("Error en fetchRestaurants", error);
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const handleOpenScheduleModal = (restaurantId: number) => {
    setSelectedRestaurantIdForSchedule(restaurantId);
  };

  const handleCloseScheduleModal = () => {
    setSelectedRestaurantIdForSchedule(null);
  };

  const handleOpenReservationModal = (restaurantId: number) => {
    setSelectedRestaurantIdForReservation(restaurantId);
  };

  const handleCloseReservationModal = () => {
    setSelectedRestaurantIdForReservation(null);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Hacer una Reserva</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
          gap: "1rem",
          marginTop: "2rem",
        }}
      >
        {restaurants.map((restaurant) => (
          <div
            key={restaurant.restaurant_id}
            style={{
              border: "1px solid gray",
              padding: "1rem",
              borderRadius: "8px",
            }}
          >
            <h2>{restaurant.name}</h2>
            <p>{restaurant.description}</p>
            <p>
              <strong>Tipo:</strong> {restaurant.restaurant_type}
            </p>
            <p>
              <strong>Teléfono:</strong> {restaurant.phone_number}
            </p>
            <p>
              <strong>Dirección:</strong> {restaurant.address}
            </p>

            <div
              style={{
                marginTop: "1rem",
                display: "flex",
                flexDirection: "column",
                gap: "0.5rem",
              }}
            >
              <button
                onClick={() =>
                  handleOpenScheduleModal(restaurant.restaurant_id)
                }
              >
                Ver Horarios
              </button>

              <button
                onClick={() =>
                  handleOpenReservationModal(restaurant.restaurant_id)
                }
              >
                Reservar
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedRestaurantIdForSchedule !== null && (
        <ScheduleModal
          restaurantId={selectedRestaurantIdForSchedule}
          onClose={handleCloseScheduleModal}
        />
      )}

      {selectedRestaurantIdForReservation !== null && (
        <ReservationModal
          restaurantId={selectedRestaurantIdForReservation}
          onClose={handleCloseReservationModal}
        />
      )}
    </div>
  );
};

export default MakeReservation;
