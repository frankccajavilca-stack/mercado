
import { useState } from "react";
import PaymentService from "../../services/paymentService";

export default function PaymentForm(){
    const [contactId, setContactId] = useState("");
    const [title, setTitle] = useState("");
    const [pago, setPago] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [mensaje, setMensaje] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const nuevaCita = {
            calendarId: "14SBo8gFMfQNhnhx2nLF",
            contactId: contactId,
            startTime: new Date().toISOString(),
            endTime: new Date(Date.now() + 60 * 60 * 1000).toISOString(), // +1 hora
            payment_amount: parseFloat(pago),
            locationId: "CRITCqv7ASS9xQPQ59Q",
            title: title,
            appointmentStatus: "confirmed",
            assignedUserId: "Ht7TypylStNewYEn8fAz",
            payment_description: descripcion,
        };

        try {
            await PaymentService(nuevaCita);
            setMensaje("✅ Cita creada con éxito");
            setContactId("");
            setTitle("");
            setPago("");
            setDescripcion("");
        } catch (error) {
            setMensaje("❌ Error al crear cita");
        }
    };
  return(
    <div style={{ maxWidth: "400px", margin: "auto" }}>
            <h2>Crear nueva cita</h2>

            <form onSubmit={handleSubmit} style={{
              display: "flex",
              flexDirection: "column",
              gap: "1rem"
            }}>
                <div className="card">
                  <label>Contact ID:</label>
                  <input
                      type="text"
                      value={contactId}
                      onChange={(e) => setContactId(e.target.value)}
                      required
                  />
                </div>

                <div className="card">
                  <label>Título:</label>
                  <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                  />
                </div>

                <div className="card">
                  <label>Monto de pago:</label>
                  <input
                      type="number"
                      value={pago}
                      onChange={(e) => setPago(e.target.value)}
                      required
                  />
                </div>

                <div className="card">
                  <label>Descripción del pago:</label>
                  <input
                      type="text"
                      value={descripcion}
                      onChange={(e) => setDescripcion(e.target.value)}
                      required
                  />
                </div>

                <button type="submit" style={{ marginTop: "10px" }}>
                    Crear cita
                </button>
            </form>

            {mensaje && <p>{mensaje}</p>}
        </div>
  );
}