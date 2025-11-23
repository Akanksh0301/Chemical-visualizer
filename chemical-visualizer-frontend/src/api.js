import axios from "axios";

const TOKEN = "6a5788d528d4768b63df56c2911f500879bedab7";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    Authorization: `Token ${TOKEN}`,
  },
});
