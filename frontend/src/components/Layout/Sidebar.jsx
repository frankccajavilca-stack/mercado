import React from "react";
import { NavLink } from "react-router-dom";
export default function Sidebar(){
  return (
    <aside className="app-sidebar">
      <ul>
        <li><NavLink to="/" className={({isActive})=> isActive ? 'active' : ''}>Dashboard</NavLink></li>
        <li><a href="#">Pagos</a></li>
        <li><a href="#">Reportes</a></li>
        <li style={{marginTop:20}}><small style={{color:'#6b7280'}}>Demo local</small></li>
      </ul>
    </aside>
  );
}