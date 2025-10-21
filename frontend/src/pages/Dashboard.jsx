import React from "react";
import PaymentList from '../components/Payment/PaymentList';
import CreatePaymentForm from '../components/Payment/CreatePaymentForm';
import { useEffect, useState } from 'react';
import api from '../services/api';

export default function Dashboard(){
  const [stats, setStats] = useState({ total:0, aprobados:0, pendientes:0 });
  useEffect(()=>{
    api.get('/payments/').then(res=>{
      const pagos = Array.isArray(res.data) ? res.data : [];
      setStats({
        total: pagos.length,
        aprobados: pagos.filter(p=>p.status==='aprobado').length,
        pendientes: pagos.filter(p=>p.status==='pendiente').length
      });
    }).catch(()=> {
      // no backend -> demo data
      const pagos = [
        {payment_id: 'p_001', contact_id: 'c_01', amount: 50, status: 'aprobado'},
        {payment_id: 'p_002', contact_id: 'c_02', amount: 20, status: 'pendiente'},
        {payment_id: 'p_003', contact_id: 'c_03', amount: 75, status: 'rejected'}
      ];
      setStats({
        total: pagos.length,
        aprobados: pagos.filter(p=>p.status==='aprobado').length,
        pendientes: pagos.filter(p=>p.status==='pendiente').length
      });
    });
  }, []);

  return (
    <div className="container">
      <h2 style={{marginBottom:12}}>Dashboard</h2>
      <div className="stats-grid">
        <div className="card">
          <h3>Total de pagos</h3>
          <div className="value">{stats.total}</div>
        </div>
        <div className="card">
          <h3>Aprobados</h3>
          <div className="value">{stats.aprobados}</div>
        </div>
        <div className="card">
          <h3>Pendientes</h3>
          <div className="value">{stats.pendientes}</div>
        </div>
      </div>

      <CreatePaymentForm />
      <PaymentList />
    </div>
  );
}