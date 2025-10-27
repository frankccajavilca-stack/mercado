import { useEffect, useState } from "react";
import PaymentButton from "./PaymentButton";
import api from "../../services/api";

export default function PaymentForm({ payment_id, clienteId, Monto, Estado }) {
  const [payment, setPayment] = useState(null);

  const statusClass = (s) =>
    s === "aprobado"
      ? "status-pill status-approved"
      : s === "pendiente"
      ? "status-pill status-pending"
      : "status-pill status-rejected";

  useEffect(() => {
    if (!payment_id) return;

    const url = `/payments/${payment_id}`;
    api
      .get(url)
      .then((res) => setPayment(res.data))
      .catch(() => {
        console.warn("Por el momento el backend no está disponible");
        const fakePayment = {
          payment_id,
          contact_id: clienteId,
          amount: Monto,
          status: Estado || "pendiente",
        };
        setPayment(fakePayment);
      });
  }, [payment_id, clienteId, Monto, Estado]);

  if (!payment) return <p>Cargando datos...</p>;

  return (
    <form
      className="card"
      style={{
        marginTop: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
        width: "30rem",
        marginInline: "auto",
      }}
    >
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
            background: "transparent",
          }}
          className={statusClass(payment.status)}
          value={payment.status}
          readOnly
        />
      </div>

      <PaymentButton paymentData={payment} />
    </form>
  );
}
