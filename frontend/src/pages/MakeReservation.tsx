import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
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
  const [selectedRestaurantId, setSelectedRestaurantId] = useState<
    number | null
  >(null);
  const navigate = useNavigate();

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

  const handleReserve = (restaurantId: number) => {
    navigate(`/reserve/${restaurantId}`);
  };

  const handleOpenModal = (restaurantId: number) => {
    setSelectedRestaurantId(restaurantId);
  };

  const handleCloseModal = () => {
    setSelectedRestaurantId(null);
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
              <button onClick={() => handleOpenModal(restaurant.restaurant_id)}>
                Ver Horarios
              </button>

              <button onClick={() => handleReserve(restaurant.restaurant_id)}>
                Reservar
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedRestaurantId !== null && (
        <ScheduleModal
          restaurantId={selectedRestaurantId}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default MakeReservation;
