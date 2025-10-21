
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
            <a href="#">Pagos</a> 
          </li>
          
          <li>
            <a href="#">Reportes</a>
          </li>
      </ul>
      
    </aside>
  ); 
}