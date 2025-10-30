
import React from "react";
import PaymentList from '../components/Payment/PaymentList';
import PaymentForm from "../components/Payment/PaymentForm";
import { useEffect, useState } from 'react';
import api from '../services/api';

export default function Dashboard(){ 
  const [stats,setStats]=useState({total:0,aprobados:0,rechazados:0,pendientes:0}); 
  useEffect(()=>{ 
    api.get('/payments/')
    .then(res=>{ const pagos=Array.isArray(res.data)?res.data:[]; 
      setStats({ 
        total:pagos.length, 
        aprobados:pagos.filter(p=>p.status==='aprobado').length,
        rechazados: pagos.filter(p => p.status === 'rechasados').length, 
        pendientes:pagos.filter(p=>p.status==='pendiente').length }); 
      })
    .catch(()=>{ 
      const pagos=[ 
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'aprobado'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'},
        {payment_id:'APPT001',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'rechazados'},
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'aprobado'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'},
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'rechazados'},
        {payment_id:'ak3K3VcPU0iP454OgAVa',contact_id:'ak3K3VcPU0iP454OgAVa',amount:150,status:'aprobado'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'pendiente'}, 
        {payment_id:'rCm2VOMTuHbIt5G3aP5h',contact_id:'rCm2VOMTuHbIt5G3aP5h',amount:150,status:'rechazados'}
      ]; 
      setStats({ 
        total:pagos.length, 
        aprobados:pagos.filter(p=>p.status==='aprobado').length, 
        rechazados: pagos.filter(p => p.status === 'rechazados').length,
        pendientes:pagos.filter(p=>p.status==='pendiente').length 
      }); 
    }); 
  },[]);

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
          <div className="value">
            {stats.aprobados}
          </div>
        </div>
        <div className="card">
          <h3>Rechazados</h3>
          <div className="value">
            {stats.rechazados}
          </div>
        </div>
        <div className="card">
          <h3>Pendientes</h3>
          <div className="value">
            {stats.pendientes}
          </div>
        </div>
      </div>
          <PaymentList/>
    </div>
    ); 
    
 }