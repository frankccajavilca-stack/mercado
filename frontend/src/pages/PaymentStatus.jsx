" yooooo Edwin "

import Logo from "../assets/logo.jpg";
import { useState , useEffect} from "react";
import api from "../services/api";


export default function PaymentStatus(){

    /** datos */
    const[ payment_id , setPayment_id] = useState("");
    const[ appointmentId , setAppointmentId] = useState("");
    const[ contactId , setContactId] = useState("");
    const[ amount , setAmount] = useState("");
    const[ description , setdescription] = useState("");

    /** metodos */
    const handleSubmit = async (e) => {
        e.preventDefault();

        if(!payment_id || !appointmentId || !contactId || !amount || !description){
            console.error("Debes completar todos los campos.");
        } else{
            
            try{
                const envioResponse = await api.post("/api/payments/create/", {
                    appointmentId,
                    contactId,
                    amount,
                    description
                });

                // Mostrar respuesta del backend
                console.log("Respuesta:", envioResponse.data);

                // Actualizar estado con datos recibidos
                setPayment_id(envioResponse.data.payment_id);

                alert("Pago creado correctamente ✅");

            } catch{
                alert("Error al momento de pago");
                console.error("Error al momento de pago");
                console.warn("Backend no disponible, usando datos falsos...");
                const fakeResponse = { data: { payment_id: "fake_001" } };

                setPayment_id(fakeResponse.data.payment_id);
                setAppointmentId("");
                setContactId("");
                setAmount("");
                setdescription("");
            }
        }

    };

    return(
        <div className="card"
            style={{
                display: "grid",
                gridTemplateColumns: "repeat(2,1fr)",
                placeItems: "center"
            }}
        >
            <div className="card-left"
                style={{
                    width: "80%"
                }}
            >
                <img src={Logo} alt="logo" width="100%"/>
            </div>
            <div className="card-right"
                style={{
                    height: "100%",
                    width: "100%",
                }}
            >
                <form onSubmit={handleSubmit} className="card" style={{
                    height: "100%",
                    width: "100%",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    textAlign: "center",
                    gap: "1rem"
                }}>
                    <h1>Completar pago</h1>

                    <div className="inputs">
                        <input 
                            type="number"
                            className="PayFormInput"
                            value={payment_id || ""}
                            onChange={(e) => setPayment_id(e.target.value)} 
                            placeholder="ID del cliente"
                            required
                        />
                        <input 
                            type="text"
                            className="PayFormInput"
                            value={appointmentId || ""}
                            onChange={(e) => setAppointmentId(e.target.value)} 
                            placeholder="zzz"
                            required
                        />
                        <input 
                            type="text"
                            className="PayFormInput"
                            value={contactId || ""}
                            onChange={(e) => setContactId(e.target.value)} 
                            placeholder="contactoId"
                            required
                        />
                        <input 
                            type="number"
                            className="PayFormInput"
                            value={amount || ""}
                            onChange={(e) => setAmount(e.target.value)} 
                            placeholder="monto"
                            required
                        />
                        <input 
                            type="text"
                            className="PayFormInput"
                            value={description || ""}
                            onChange={(e) => setdescription(e.target.value)} 
                            placeholder="Descripción"
                            required
                        />
                    </div>
                    <button type="submit" className="btn-pago-register">Completar</button>
                </form>

                {payment_id && (
                    <p style={{ marginTop: "10px" }}>
                        <strong>ID de Pago:</strong> {payment_id}
                    </p>
                )}
            </div>
        </div>
    );
}