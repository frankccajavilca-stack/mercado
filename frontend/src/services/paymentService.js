// src/services/paymentService.js

const urlPost = "http://127.0.0.1:8000/api/appointments/create/";
const token = import.meta.env.VITE_GHL_ACCESS_TOKEN; // ✅ tu token del .env

async function PaymentService(nuevaCita) {
    try {
        const respuesta = await fetch(urlPost, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // 🔥 aquí agregas el token
            },
            body: JSON.stringify(nuevaCita),
        });

        if (!respuesta.ok) {
            throw new Error(`Error ${respuesta.status}: no se pudo crear la cita`);
        }

        const data = await respuesta.json();
        console.log("✅ Cita creada correctamente:", data);
        console.log("Token usado (frontend):", token);
        return data;
    } catch (error) {
        console.error("❌ Error en PaymentService:", error);
        throw error;
    }
}

export default PaymentService;
