import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Layout/Header";
import Sidebar from "./components/Layout/Sidebar";
import Dashboard from "./pages/dashboard";
import PaymentForm from "./components/Payment/PaymentForm";

export default function App(){
  return (
    <Router>
      <Header />
      <Sidebar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/registrar" element={<PaymentForm />} />
        </Routes>
      </main>
    </Router>
  );
}