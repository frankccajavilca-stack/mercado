" yooooo Edwin "

// paymentService.js

import Api from "./api";

export async function getPaymentById(id) {
  const res = await Api.get(`/payments/${id}`);
  return res.data;
}

export async function createPayment(paymentData) {
  const res = await Api.post("/payments", paymentData);
  return res.data;
}
