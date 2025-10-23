
import React from "react";
import { useEffect, useState } from "react";
import api from "../../services/api";

export default function PaymentList(){ 

  const [payments,setPayments]=useState([]); 
  
  useEffect(()=>{ 
    api.get('/payments/')
    .then(res=>setPayments(Array.isArray(res.data)?res.data:[]))
    .catch(()=>setPayments([ 
      {payment_id:'p_001',contact_id:'c_01',amount:50,status:'aprobado'}, 
      {payment_id:'p_002',contact_id:'c_02',amount:20,status:'pendiente'}, 
      {payment_id:'p_003',contact_id:'c_03',amount:75,status:'rechazado'},
      {payment_id:'p_004',contact_id:'c_04',amount:90,status:'rechazado'} 
    ])); 
  },[]); 
  
  const statusClass = (s) => s=== 'aprobado' ? 'status-pill status-approved':s=== 'pendiente' ? 'status-pill status-pending' : 'status-pill status-rejected'; 
  
  return (
  <div className="card" style={{marginTop:12}}>
    <h3>Lista de pagos recientes</h3>
    <table className="payments-table" aria-label="Pagos">

      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Monto</th>
          <th>Estado</th>
        </tr>
      </thead>
      
      <tbody>
        {payments.map(p=>(
          <tr key={p.payment_id||p.id}>
            <td>{p.payment_id||p.id}</td>
            <td>{p.contact_id}</td>
            <td>${p.amount}</td>
            <td>
              <span className={statusClass(p.status)}>{p.status}</span>
            </td>
          </tr>))}
      </tbody>
      
    </table>
  </div>
  ); 
}