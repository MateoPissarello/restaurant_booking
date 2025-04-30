import React from "react";

interface DeleteConfirmationModalProps {
  booking: {
    booking_id: number;
  };
  onClose: () => void;
  onUpdate: () => void;
}

const DeleteConfirmationModal: React.FC<DeleteConfirmationModalProps> = ({
  booking,
  onClose,
  onUpdate,
}) => {
  const handleDelete = async () => {
    try {
      const response = await fetch(`http://localhost:8000/booking/delete/admin/${booking.booking_id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (response.ok) {
        alert("Reserva eliminada exitosamente.");
        onUpdate(); // Refrescar listado de reservas
        onClose();  // Cerrar el modal
      } else {
        alert("Error al eliminar la reserva.");
      }
    } catch (error) {
      console.error("Error en handleDelete:", error);
      alert("Error al eliminar la reserva.");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
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
        <h2>Confirmar Eliminación</h2>
        <p>¿Estás seguro que deseas eliminar esta reserva?</p>

        <div style={{ marginTop: "1.5rem", display: "flex", gap: "1rem" }}>
          <button onClick={handleDelete} style={{ backgroundColor: "red", color: "white" }}>
            Confirmar
          </button>
          <button onClick={onClose}>Cancelar</button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmationModal;
