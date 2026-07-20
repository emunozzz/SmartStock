import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../components/common/DashboardLayout";
import { listarProductos } from "../api/productoService";
import { listarClientes } from "../api/clienteService";
import { registrarVenta } from "../api/ventaService";

const ITBMS_RATE = 0.07;

export default function Ventas() {
  const [productos, setProductos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [busqueda, setBusqueda] = useState("");
  const [carrito, setCarrito] = useState([]); // [{ producto_id, nombre, cantidad, precio_unitario, stock_disponible }]
  const [clienteId, setClienteId] = useState("");

  const [procesando, setProcesando] = useState(false);
  const [mensaje, setMensaje] = useState(null); // { tipo: "success" | "error", texto }

  useEffect(() => {
    async function cargar() {
      setLoading(true);
      setError(null);
      try {
        const [prods, clis] = await Promise.all([
          listarProductos(),
          listarClientes().catch(() => []), // el módulo de clientes es opcional para la caja
        ]);
        setProductos(prods.filter((p) => p.activo));
        setClientes(clis);
        if (clis.length > 0) setClienteId(String(clis[0].cliente_id));
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    cargar();
  }, []);

  const productosFiltrados = useMemo(() => {
    const term = busqueda.trim().toLowerCase();
    if (!term) return productos;
    return productos.filter((p) => p.nombre.toLowerCase().includes(term));
  }, [productos, busqueda]);

  const subtotal = useMemo(
    () =>
      carrito.reduce(
        (acc, item) => acc + item.precio_unitario * item.cantidad,
        0
      ),
    [carrito]
  );
  const itbms = subtotal * ITBMS_RATE;
  const total = subtotal + itbms;

  function agregarAlCarrito(producto) {
    setCarrito((prev) => {
      const existente = prev.find((i) => i.producto_id === producto.producto_id);
      if (existente) {
        return prev.map((i) =>
          i.producto_id === producto.producto_id
            ? { ...i, cantidad: i.cantidad + 1 }
            : i
        );
      }
      return [
        ...prev,
        {
          producto_id: producto.producto_id,
          nombre: producto.nombre,
          cantidad: 1,
          precio_unitario: Number(producto.precio_venta),
        },
      ];
    });
  }

  function cambiarCantidad(productoId, cantidad) {
    const cantidadNumerica = Math.max(1, Number(cantidad) || 1);
    setCarrito((prev) =>
      prev.map((i) =>
        i.producto_id === productoId ? { ...i, cantidad: cantidadNumerica } : i
      )
    );
  }

  function quitarDelCarrito(productoId) {
    setCarrito((prev) => prev.filter((i) => i.producto_id !== productoId));
  }

  async function procesarVenta() {
    setMensaje(null);

    if (carrito.length === 0) {
      setMensaje({ tipo: "error", texto: "Agrega al menos un producto al carrito." });
      return;
    }
    if (!clienteId) {
      setMensaje({ tipo: "error", texto: "Selecciona un cliente para la venta." });
      return;
    }

    setProcesando(true);
    try {
      await registrarVenta({
        cliente_id: Number(clienteId),
        detalles: carrito.map((i) => ({
          producto_id: i.producto_id,
          cantidad: i.cantidad,
          precio_unitario: i.precio_unitario,
        })),
      });
      setMensaje({ tipo: "success", texto: "Venta registrada correctamente." });
      setCarrito([]);
    } catch (err) {
      setMensaje({ tipo: "error", texto: err.message || "No se pudo procesar la venta." });
    } finally {
      setProcesando(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-5">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Ventas / Caja</h2>
          <p className="text-sm text-slate-500">
            Selecciona productos para armar la venta y procésala al finalizar.
          </p>
        </div>

        {loading && <p className="text-sm text-slate-400">Cargando catálogo...</p>}
        {!loading && error && (
          <p className="text-sm text-red-600">
            No se pudo cargar el catálogo: {error}
          </p>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            {/* Columna izquierda: buscador y catálogo */}
            <div className="lg:col-span-3 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <div className="p-4 border-b border-slate-100">
                <input
                  type="text"
                  placeholder="Buscar producto por nombre..."
                  value={busqueda}
                  onChange={(e) => setBusqueda(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                />
              </div>

              <div className="max-h-[520px] overflow-y-auto divide-y divide-slate-100">
                {productosFiltrados.map((p) => (
                  <button
                    key={p.producto_id}
                    onClick={() => agregarAlCarrito(p)}
                    className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-emerald-50 transition-colors"
                  >
                    <div>
                      <p className="text-sm font-medium text-slate-800">
                        {p.nombre}
                      </p>
                      <p className="text-xs text-slate-400">
                        {p.unidad_medida}
                      </p>
                    </div>
                    <span className="text-sm font-semibold text-slate-700">
                      ${Number(p.precio_venta).toFixed(2)}
                    </span>
                  </button>
                ))}

                {productosFiltrados.length === 0 && (
                  <p className="px-4 py-8 text-center text-sm text-slate-400">
                    No se encontraron productos.
                  </p>
                )}
              </div>
            </div>

            {/* Columna derecha: carrito / resumen de venta */}
            <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl shadow-sm flex flex-col">
              <div className="p-4 border-b border-slate-100">
                <h3 className="text-sm font-semibold text-slate-900">
                  Venta actual
                </h3>

                <label className="block text-xs font-medium text-slate-600 mt-3 mb-1">
                  Cliente
                </label>
                {clientes.length > 0 ? (
                  <select
                    value={clienteId}
                    onChange={(e) => setClienteId(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  >
                    {clientes.map((c) => (
                      <option key={c.cliente_id} value={c.cliente_id}>
                        {c.nombre}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="number"
                    min="1"
                    placeholder="ID del cliente"
                    value={clienteId}
                    onChange={(e) => setClienteId(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                )}
              </div>

              <div className="flex-1 overflow-y-auto divide-y divide-slate-100 max-h-80">
                {carrito.length === 0 && (
                  <p className="px-4 py-8 text-center text-sm text-slate-400">
                    Aún no has agregado productos.
                  </p>
                )}

                {carrito.map((item) => (
                  <div
                    key={item.producto_id}
                    className="flex items-center justify-between px-4 py-3 gap-2"
                  >
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-800 truncate">
                        {item.nombre}
                      </p>
                      <p className="text-xs text-slate-400">
                        ${item.precio_unitario.toFixed(2)} c/u
                      </p>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <input
                        type="number"
                        min="1"
                        value={item.cantidad}
                        onChange={(e) =>
                          cambiarCantidad(item.producto_id, e.target.value)
                        }
                        className="w-16 rounded-lg border border-slate-300 px-2 py-1 text-sm text-center focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      />
                      <button
                        onClick={() => quitarDelCarrito(item.producto_id)}
                        className="text-slate-400 hover:text-red-600 text-sm"
                        aria-label={`Quitar ${item.nombre}`}
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-4 border-t border-slate-100 space-y-1.5">
                <div className="flex justify-between text-sm text-slate-600">
                  <span>Subtotal</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm text-slate-600">
                  <span>ITBMS (7%)</span>
                  <span>${itbms.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-base font-semibold text-slate-900 pt-1.5 border-t border-slate-100">
                  <span>Total</span>
                  <span>${total.toFixed(2)}</span>
                </div>

                {mensaje && (
                  <div
                    className={`rounded-lg text-sm px-3 py-2 mt-2 ${
                      mensaje.tipo === "success"
                        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                        : "bg-red-50 text-red-700 border border-red-200"
                    }`}
                  >
                    {mensaje.texto}
                  </div>
                )}

                <button
                  onClick={procesarVenta}
                  disabled={procesando}
                  className="w-full mt-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white text-sm font-medium py-2.5 transition-colors"
                >
                  {procesando ? "Procesando..." : "Procesar venta"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
