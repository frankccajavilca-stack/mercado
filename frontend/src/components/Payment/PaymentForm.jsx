" yooooo Edwin "
import { useEffect , useState } from "react";
import PaymentButton from "./PaymentButton";
import api from "../../services/api"

export default function PaymentForm({ payment_id }){

    /**  datos */
    const [ payment , setPayment ] = useState(null);
    const statusClass = (s) => s=== 'aprobado' ? 'status-pill status-approved':s=== 'pendiente' ? 'status-pill status-pending' : 'status-pill status-rejected';

    /** peticion al backend */
    useEffect(() => {
        // if(!payment_id) return;

        const url = `/payments/${payment_id}`;
        api.get(url)
            .then(res => setPasetPaymentyment(res.data))
            .catch(()=> {
                console.warn("Por el momento el banckend no esta disponible");
                const fakePayment = {
                    payment_id: "p_001",
                    contact_id: "c_01",
                    amount: 10,
                    status: "pendiente",
                };

                setPayment(fakePayment);               
            });
    },[payment_id]);

    if(!payment) return <p>Cargando datos...</p>;

    return(
        <form action="" className="card" 
            style={{
                    marginTop: "2rem", 
                    display: "flex", 
                    flexDirection: "column", 
                    gap: "1rem",
                    width: "30rem",                    
                }}>

            <div className="inputs">
                <input 
                    type="text"
                    className="PayFormInput"
                    value={payment.payment_id}
                    readOnly
                />
                <input 
                    type="text"
                    className="PayFormInput"
                    value={payment.contact_id}
                    readOnly
                />
                <input 
                    type="text"
                    className="PayFormInput"
                    value={`$${payment.amount}`}
                    readOnly
                />
                <input 
                    type="text"
                    style={{
                        border: "none",
                        textAlign: "center",
                        borderRadius: "none",
                    }}
                    className={statusClass()}
                    value={payment.status}
                    readOnly
                />
                </div>

            <PaymentButton paymentData={payment}/>

        </form>
    );
}