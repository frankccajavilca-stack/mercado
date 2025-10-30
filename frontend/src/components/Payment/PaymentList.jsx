import React, { useEffect, useState } from "react";
import api from "../../services/api";
import PaymentForm from "./PaymentForm";

export default function PaymentList() {
  const [payments, setPayments] = useState([]);
  const [verDetalles, setVerDetalles] = useState(null); // guarda el ID del pago mostrado

  useEffect(() => {
    api
      .get("/payments/")
      .then((res) => setPayments(Array.isArray(res.data) ? res.data : []))
      .catch(() =>
        setPayments([
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'aprobado'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'},
        {payment_id:'APPT001',contact_id:'CONTACT001',amount:150,status:'rechazados'},
        {payment_id:'APPT002',contact_id:'CONTACT002',amount:150,status:'aprobado'}, 
        {payment_id:'APPT003',contact_id:'CONTACT003',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'},
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'rechazados'},
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'aprobado'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'}
         
        ])
      );
  }, []);

  const statusClass = (s) =>
    s === "aprobado"
      ? "status-pill status-approved"
      : s === "pendiente"
      ? "status-pill status-pending"
      : "status-pill status-rejected";

  const handleVerClick = (id) => {
    // si haces clic en el mismo ID, se oculta
    setVerDetalles(verDetalles === id ? null : id);
  };

  return (
    <div className="card" style={{ marginTop: 12 }}>
      <h3>Lista de pagos recientes</h3>
      <table className="payments-table" aria-label="Pagos" style={{ width: "100%", textAlign: "center" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Monto</th>
            <th>Estado</th>
            <th>.</th>
          </tr>
        </thead>

        <tbody>
          {payments.map((p) => (
            <React.Fragment key={p.payment_id || p.id}>
              <tr>
                <td>{p.payment_id || p.id}</td>
                <td>{p.contact_id}</td>
                <td>${p.amount}</td>
                <td>
                  <span className={statusClass(p.status)}>{p.status}</span>
                </td>
                <td>
                  <button className="btn-ver-list" onClick={() => handleVerClick(p.payment_id)}>
                    {verDetalles === p.payment_id ? "Ocultar" : "Ver"}
                  </button>
                </td>
              </tr>

              {/* Mostrar el formulario debajo SOLO si coincide el ID */}
              {verDetalles === p.payment_id && (
                <tr>
                  <td colSpan="5">
                    <PaymentForm 
                      payment_id={p.payment_id}
                      clienteId={p.contact_id}
                      Monto={p.amount}
                    />
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
