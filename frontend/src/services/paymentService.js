" yooooo Edwin "

// paymentService.js

import api from "./api";

export async function getPaymentById(id) {
  const res = await api.get(`/payments/${id}`);
  return res.data;
}

export async function createPayment(paymentData) {
  const res = await api.post("/payments", paymentData);
  return res.data;
}
