import { useEffect, useState } from "react";

interface Schedule {
  schedule_id: number;
  restaurant_id: number;
  day: string;
  opening_hour: string;
  closing_hour: string;
}

interface ScheduleModalProps {
  restaurantId: number;
  onClose: () => void;
}

const ScheduleModal: React.FC<ScheduleModalProps> = ({
  restaurantId,
  onClose,
}) => {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:8000/schedule/get/${restaurantId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Error fetching schedules");
        }

        const data = await response.json();
        setSchedules(data);
      } catch (error) {
        console.error(error);
        alert("Error al obtener horarios");
      } finally {
        setLoading(false);
      }
    };

    fetchSchedules();
  }, [restaurantId]);

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          padding: "2rem",
          borderRadius: "8px",
          minWidth: "300px",
        }}
      >
        <h2>Horarios del Restaurante</h2>
        {loading ? (
          <p>Cargando horarios...</p>
        ) : (
          <div>
            {schedules.length === 0 ? (
              <p>No hay horarios disponibles.</p>
            ) : (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {schedules.map((schedule) => (
                  <li
                    key={schedule.schedule_id}
                    style={{ marginBottom: "1rem" }}
                  >
                    <strong>{capitalize(schedule.day)}</strong>:{" "}
                    {schedule.opening_hour} - {schedule.closing_hour}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
        <button onClick={onClose} style={{ marginTop: "1rem" }}>
          Cerrar
        </button>
      </div>
    </div>
  );
};

// Función utilitaria para poner mayúscula al primer carácter del día
function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export default ScheduleModal;
