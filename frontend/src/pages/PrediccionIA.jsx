import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import DashboardLayout from "../components/common/DashboardLayout";
import { getPrediccionDemanda } from "../api/prediccionService";

export default function PrediccionIA() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPrediccionDemanda()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Predicción de demanda
            </h2>
            <p className="text-sm text-slate-500">
              Proyección estimada por IA para los próximos meses.
            </p>
          </div>
          <span className="inline-flex items-center rounded-full bg-emerald-50 text-emerald-700 text-xs font-medium px-2.5 py-1">
            Datos reales — Groq + Llama 3.3
          </span>
        </div>

        {loading && <p className="text-sm text-slate-400">Cargando predicción...</p>}
        {!loading && error && (
          <p className="text-sm text-red-600">
            No se pudo cargar la predicción: {error}
          </p>
        )}

        {!loading && !error && data && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
                <p className="text-xs font-medium text-slate-500">
                  Producto con mayor tendencia de demanda
                </p>
                <p className="text-lg font-semibold text-slate-900 mt-2">
                  {data.insights.producto_mayor_tendencia.nombre}
                </p>
                <p className="text-sm text-emerald-600 font-medium mt-1">
                  ▲ {data.insights.producto_mayor_tendencia.variacion_pct}% vs. mes anterior
                </p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
                <p className="text-xs font-medium text-slate-500">
                  Riesgo de quiebre de stock
                </p>
                <p className="text-lg font-semibold text-slate-900 mt-2">
                  {data.insights.producto_riesgo_quiebre.nombre}
                </p>
                <p className="text-sm text-red-600 font-medium mt-1">
                  Se agota en ~{data.insights.producto_riesgo_quiebre.dias_restantes_stock} días
                </p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
                <p className="text-xs font-medium text-slate-500">
                  Precisión del modelo
                </p>
                <p className="text-lg font-semibold text-slate-900 mt-2">
                  {data.insights.precision_modelo_pct}%
                </p>
                <p className="text-sm text-slate-400 mt-1">
                  Sobre datos históricos de validación
                </p>
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
              <h3 className="text-sm font-semibold text-slate-900 mb-1">
                Demanda histórica vs. proyectada
              </h3>
              <p className="text-xs text-slate-500 mb-4">
                Unidades estimadas por mes — datos reales del backend con IA
              </p>

              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data.proyeccion} margin={{ left: -10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis
                      dataKey="periodo"
                      stroke="#64748b"
                      fontSize={12}
                    />
                    <YAxis stroke="#64748b" fontSize={12} />
                    <Tooltip
                      contentStyle={{
                        borderRadius: 8,
                        border: "1px solid #e2e8f0",
                        fontSize: 13,
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: 13 }} />
                    <Line
                      type="monotone"
                      dataKey="demanda_historica"
                      name="Histórico"
                      stroke="#6366f1"
                      strokeWidth={2}
                      dot={{ r: 3 }}
                      connectNulls
                    />
                    <Line
                      type="monotone"
                      dataKey="demanda_proyectada"
                      name="Proyectado"
                      stroke="#059669"
                      strokeWidth={2}
                      strokeDasharray="5 4"
                      dot={{ r: 3 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
