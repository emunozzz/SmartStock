import { useEffect, useState } from "react";
import DashboardLayout from "../components/common/DashboardLayout";
import KpiCard from "../components/dashboard/KpiCard";
import StockAlerts from "../components/dashboard/StockAlerts";
import { listarProductos } from "../api/productoService";
import { getAlertasStockBajo } from "../api/inventarioService";
import { listarVentas } from "../api/ventaService";
import { listarCompras } from "../api/compraService";

/**
 * Intenta encontrar un campo de fecha en un registro de venta/compra,
 * probando los nombres más comunes. Si el backend usa otro nombre,
 * "esDeHoy" simplemente no podrá filtrar por día y el KPI cae de vuelta
 * al total registrado (ver más abajo).
 */
function obtenerFecha(registro) {
  return (
    registro.fecha_venta ||
    registro.fecha_creacion ||
    registro.fecha ||
    registro.created_at ||
    null
  );
}

function esDeHoy(fechaStr) {
  if (!fechaStr) return false;
  const fecha = new Date(fechaStr);
  if (Number.isNaN(fecha.getTime())) return false;
  const hoy = new Date();
  return fecha.toDateString() === hoy.toDateString();
}

export default function Dashboard() {
  const [productos, setProductos] = useState([]);
  const [alertas, setAlertas] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [compras, setCompras] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    async function cargarKpis() {
      // Cada fetch va por separado y con su propio catch: si un módulo
      // todavía no tiene datos (o su endpoint falla), el resto del panel
      // se sigue mostrando en vez de quedar todo en blanco.
      const [prods, alrt, vts, cmps] = await Promise.all([
        listarProductos().catch(() => []),
        getAlertasStockBajo().catch(() => []),
        listarVentas().catch(() => []),
        listarCompras().catch(() => []),
      ]);
      setProductos(prods);
      setAlertas(alrt);
      setVentas(vts);
      setCompras(cmps);
      setCargando(false);
    }
    cargarKpis();
  }, []);

  const productosActivos = productos.filter((p) => p.activo).length;

  const ventasConFecha = ventas.filter((v) => obtenerFecha(v));
  const hayFechaEnVentas = ventasConFecha.length > 0;
  const ventasHoy = ventas.filter((v) => esDeHoy(obtenerFecha(v))).length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Panel general
          </h2>
          <p className="text-sm text-slate-500">
            Resumen de la operación e inventario en tiempo real.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard
            label="Productos activos"
            value={cargando ? "—" : productosActivos}
            hint={cargando ? undefined : `${productos.length} en catálogo total`}
          />
          <KpiCard
            label={hayFechaEnVentas ? "Ventas de hoy" : "Ventas registradas"}
            value={cargando ? "—" : hayFechaEnVentas ? ventasHoy : ventas.length}
            tone="positive"
          />
          <KpiCard
            label="Compras registradas"
            value={cargando ? "—" : compras.length}
            tone="warning"
          />
          <KpiCard
            label="Productos en alerta"
            value={cargando ? "—" : alertas.length}
            tone="critical"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <StockAlerts />
          </div>
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
            <h2 className="text-sm font-semibold text-slate-900">
              Próximos pasos
            </h2>
            <ul className="mt-3 space-y-2 text-sm text-slate-600 list-disc list-inside">
              <li>Conectar reportes y gráficas de tendencias (QA)</li>
              <li>Confirmar el endpoint real de predicción de demanda</li>
              <li>Definir un estado "pendiente" para compras, si aplica</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
