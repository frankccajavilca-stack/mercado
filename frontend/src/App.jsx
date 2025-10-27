import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Layout/Header";
import Sidebar from "./components/Layout/Sidebar";
import Dashboard from "./pages/dashboard";
import AdminDashboard from "./pages/AdminDashboard";
import Status from "./components/Payment/StatusBanner";
import PaymentStatus from "./pages/PaymentStatus";

export default function App(){
  return (
    <Router>
      <Header />
      <Sidebar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/registrar" element={<PaymentStatus />} />
          <Route path="/reportes" element={<Status />} />
        </Routes>
      </main>
    </Router>
  );
}