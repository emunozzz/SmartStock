import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

/**
 * Envuelve las rutas privadas del dashboard. Si no hay sesión activa,
 * redirige a /login conservando la ruta de origen (útil para volver
 * al lugar correcto después de iniciar sesión).
 */
export default function ProtectedRoute() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
