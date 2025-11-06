
import React from "react";
import PaymentStatus from "./PaymentStatus"
import PaymentList from '../components/Payment/PaymentList';


export default function Dashboard(){ 
  


  return (
    <div className="container">
          <PaymentStatus/>
          <br />
          <PaymentList/>
    </div>
    ); 
    
 }