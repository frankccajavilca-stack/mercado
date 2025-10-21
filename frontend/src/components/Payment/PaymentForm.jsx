" yooooo Edwin "
import { useEffect , useState } from "react";
import PaymentButton from "./PaymentButton";
import Api from "../../services/api"

export default function PaymentForm({ payment_id }){

    /**  datos */
    const [ payment , setPaymentId ] = useState(null);
    // const [ appointmentId , setAppointmentId ] = useState("");
    // const [ contactId , setContactId ] = useState(""); 
    // const [ amount , setAmount ] = useState(""); 
    // const [ description , setDescription ] = useState(""); 

    /** peticion al backend */
    useEffect(() => {
        if(!payment_id) return;

        const url = "/payments/${payment_id}";
        Api.get(url)
            .then(data => setPaymentId(data))
            .catch(error => console.error("Error encontrado => ", error));
    },[payment_id]);

    if(!payment) return <p>Cargando datos...</p>;

    return(
        <form action="">

            <input 
                type="number"
                className="PayFormInput"
                value={payment.appointmentId}
                readOnly
            />
            <input 
                type="number"
                className="PayFormInput"
                value={payment.appointmentId}
                readOnly
            />
            <input 
                type="number"
                className="PayFormInput"
                value={payment.appointmentId}
                readOnly
            />
            <input 
                type="number"
                className="PayFormInput"
                value={payment.appointmentId}
                readOnly
            />

            <PaymentButton paymentData={payment}/>

        </form>
    )
}