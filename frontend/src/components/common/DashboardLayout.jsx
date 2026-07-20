import { NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Panel general", icon: "📊" },
  { to: "/productos", label: "Productos", icon: "📦" },
  { to: "/ventas", label: "Ventas / Caja", icon: "🧾" },
  { to: "/prediccion", label: "Predicción IA", icon: "🤖" },
];

export default function DashboardLayout({ children }) {
  const navigate = useNavigate();
  const usuario = useAuthStore((state) => state.usuario);
  const logout = useAuthStore((state) => state.logout);

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <aside className="w-60 shrink-0 bg-slate-900 text-slate-200 flex flex-col">
        <div className="h-16 flex items-center gap-2 px-5 border-b border-slate-800">
          <div className="h-8 w-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold text-sm">
            S
          </div>
          <span className="font-semibold text-white text-sm">SmartStock</span>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition-colors ${
                  isActive
                    ? "bg-emerald-600 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <span aria-hidden="true">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-slate-800">
          <p className="px-3 text-xs text-slate-400 truncate">
            {usuario?.nombre || "Sesión activa"}
          </p>
          <button
            onClick={handleLogout}
            className="mt-2 w-full text-left rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
          >
            Cerrar sesión
          </button>
        </div>
      </aside>

      <main className="flex-1 min-w-0">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-6">
          <h1 className="text-sm font-medium text-slate-600">
            Sistema Inteligente de Gestión de Inventario
          </h1>
        </header>
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
