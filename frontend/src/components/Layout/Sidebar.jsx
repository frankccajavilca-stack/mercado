
import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar(){ 
 
  return (
    <aside className="app-sidebar">

      <ul style={{listStyle:'none'}}>

          <li style={{marginBottom:10}}>
            <NavLink to="/" className={({isActive})=> isActive ? 'active' : ''}>Dashboard</NavLink>
          </li>

          <li style={{marginBottom:10}}>
            <NavLink to="/admin" className={({isActive})=> isActive ? 'active' : ''}>Admin</NavLink>
          </li>

          <li style={{marginBottom:10}}>
            <NavLink to="/registrar" className={({isActive})=> isActive ? 'active' : ''}>Registrar Pagos</NavLink>
          </li>
          
          <li>
            <NavLink to="/reportes" className={({isActive})=> isActive ? 'active' : ''}>Reportes</NavLink>
          </li>
      </ul>
      
    </aside>
  ); 
}