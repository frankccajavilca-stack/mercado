import axios from "axios";

const API_URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000/api/"
    : "/api/";

const api = axios.create({
  baseURL: API_URL,
});

export default api;
