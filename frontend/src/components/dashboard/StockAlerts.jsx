import { useEffect, useState } from "react";
import { getAlertasStockBajo } from "../../api/inventarioService";

export default function StockAlerts() {
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let activo = true;

    async function fetchAlertas() {
      try {
        const data = await getAlertasStockBajo();
        if (activo) setAlertas(data);
      } catch (err) {
        if (activo) setError(err.message);
      } finally {
        if (activo) setLoading(false);
      }
    }

    fetchAlertas();
    return () => {
      activo = false;
    };
  }, []);

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm">
      <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">
            Alertas de stock bajo
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Productos por debajo del punto mínimo de reorden
          </p>
        </div>
        {!loading && alertas.length > 0 && (
          <span className="inline-flex items-center rounded-full bg-red-50 text-red-700 text-xs font-medium px-2.5 py-1">
            {alertas.length} crítico{alertas.length === 1 ? "" : "s"}
          </span>
        )}
      </div>

      <div className="p-5">
        {loading && (
          <p className="text-sm text-slate-400">Cargando alertas...</p>
        )}

        {!loading && error && (
          <p className="text-sm text-red-600">
            No se pudieron cargar las alertas: {error}
          </p>
        )}

        {!loading && !error && alertas.length === 0 && (
          <p className="text-sm text-slate-500">
            Todo el inventario está dentro de niveles saludables. ✅
          </p>
        )}

        {!loading && !error && alertas.length > 0 && (
          <ul className="divide-y divide-slate-100">
            {alertas.map((item) => (
              <li
                key={item.producto_id}
                className="flex items-center justify-between py-2.5"
              >
                <div>
                  <p className="text-sm font-medium text-slate-800">
                    {item.nombre}
                  </p>
                  <p className="text-xs text-slate-500">
                    Mínimo requerido: {item.stock_minimo} {item.unidad_medida}
                  </p>
                </div>
                <span className="text-sm font-semibold text-red-600">
                  {item.stock_actual} {item.unidad_medida}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
