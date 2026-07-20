import axios from "axios";
import { useAuthStore } from "../store/authStore";

/**
 * Instancia central de Axios para SmartStock.
 * Toda la app debe importar ESTE cliente en lugar de usar axios directamente,
 * para garantizar que el token JWT y el manejo de errores sean consistentes.
 */
const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

/**
 * INTERCEPTOR DE REQUEST
 * Inyecta automáticamente el access_token (JWT) en cada petición saliente,
 * leyéndolo desde el store de autenticación (Zustand + persist -> localStorage).
 * Así ningún componente necesita preocuparse por adjuntar el header manualmente.
 */
axiosClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * INTERCEPTOR DE RESPONSE
 * - Si el backend responde 401 (token vencido/ inválido), se cierra la sesión
 *   automáticamente y se redirige al login.
 * - Normaliza el mensaje de error para que los componentes puedan mostrarlo
 *   directamente sin parsear la forma de FastAPI (que usa { detail: "..." }).
 */
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      useAuthStore.getState().logout();
      // Evita loops de redirección si ya estamos en /login
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    const backendMessage =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      "Ocurrió un error inesperado. Intenta de nuevo.";

    return Promise.reject({
      status,
      message: Array.isArray(backendMessage)
        ? backendMessage.map((e) => e.msg).join(" | ") // errores de validación 422 de Pydantic
        : backendMessage,
      raw: error,
    });
  }
);

export default axiosClient;
