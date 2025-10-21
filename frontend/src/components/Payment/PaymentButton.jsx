" yooooo Edwin "

import { createPayment } from "../service/paymentService";

export default function PaymentButton({ paymentData }) {
  const handleClick = async () => {
    try {
      const result = await createPayment(paymentData);
      console.log("Pago registrado:", result);
      alert("✅ Pago registrado correctamente");
    } catch (error) {
      console.error(error);
      alert("❌ Error al registrar el pago");
    }
  };

  return <button onClick={handleClick}>Registrar pago</button>;
}

