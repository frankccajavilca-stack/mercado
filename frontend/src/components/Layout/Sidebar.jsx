
import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar(){ 
 
  return (
    <aside className="app-sidebar">

      <ul style={{listStyle:'none'}}>

          <li style={{marginBottom:10}}>
            <NavLink to="/" className={({isActive})=> isActive ? 'active' : ''}>Citas Registradas</NavLink>
          </li>

          <li style={{marginBottom:10}}>
            <NavLink to="/registrar" className={({isActive})=> isActive ? 'active' : ''}>Registrar Cita</NavLink>
          </li>

      </ul>
      
    </aside>
  ); 
}