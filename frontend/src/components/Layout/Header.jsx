
import React from "react";

export default function Header(){ 
  
  return (
    <header className="app-header">
      <div style={{display:'flex',alignItems:'center',gap:12}}>
        <div className="logo">PD</div>
        <div>
          <div style={{fontSize:16,fontWeight:700}}>Panel de Pagos</div>
          <div style={{fontSize:12,color:'rgba(255,255,255,0.9)'}}>Frontend 1</div>
        </div>
      </div>
          <div style={{fontSize:14}}>Admin • Fabricio</div>
    </header>
  );

}