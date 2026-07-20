import { useEffect, useMemo, useState } from "react";
import DashboardLayout from "../components/common/DashboardLayout";
import ProductoModal from "../components/productos/ProductoModal";
import {
  listarProductos,
  crearProducto,
  actualizarProducto,
  desactivarProducto,
} from "../api/productoService";
import { listarCategorias } from "../api/categoriaService";

export default function Productos() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [busqueda, setBusqueda] = useState("");
  const [filtroCategoria, setFiltroCategoria] = useState("todas");

  const [modalAbierto, setModalAbierto] = useState(false);
  const [productoEditando, setProductoEditando] = useState(null);

  async function cargarDatos() {
    setLoading(true);
    setError(null);
    try {
      const [prods, cats] = await Promise.all([
        listarProductos(),
        listarCategorias(),
      ]);
      setProductos(prods);
      setCategorias(cats);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    cargarDatos();
  }, []);

  const mapaCategorias = useMemo(() => {
    const mapa = {};
    categorias.forEach((c) => {
      mapa[c.categoria_id] = c.nombre;
    });
    return mapa;
  }, [categorias]);

  const productosFiltrados = useMemo(() => {
    return productos.filter((p) => {
      const coincideTexto = p.nombre
        .toLowerCase()
        .includes(busqueda.trim().toLowerCase());
      const coincideCategoria =
        filtroCategoria === "todas" ||
        String(p.categoria_id) === String(filtroCategoria);
      return coincideTexto && coincideCategoria;
    });
  }, [productos, busqueda, filtroCategoria]);

  function abrirCrear() {
    setProductoEditando(null);
    setModalAbierto(true);
  }

  function abrirEditar(producto) {
    setProductoEditando(producto);
    setModalAbierto(true);
  }

  async function handleGuardar(payload) {
    if (productoEditando) {
      const actualizado = await actualizarProducto(
        productoEditando.producto_id,
        payload
      );
      setProductos((prev) =>
        prev.map((p) =>
          p.producto_id === actualizado.producto_id ? actualizado : p
        )
      );
    } else {
      const nuevo = await crearProducto(payload);
      setProductos((prev) => [nuevo, ...prev]);
    }
    setModalAbierto(false);
  }

  async function handleDesactivar(producto) {
    const confirmado = window.confirm(
      `¿Desactivar "${producto.nombre}"? El historial de compras y ventas se conserva; el producto solo dejará de estar activo.`
    );
    if (!confirmado) return;

    try {
      await desactivarProducto(producto.producto_id);
      setProductos((prev) =>
        prev.map((p) =>
          p.producto_id === producto.producto_id ? { ...p, activo: false } : p
        )
      );
    } catch (err) {
      window.alert(err.message || "No se pudo desactivar el producto.");
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Productos</h2>
            <p className="text-sm text-slate-500">
              Catálogo de productos y categorías.
            </p>
          </div>
          <button
            onClick={abrirCrear}
            className="rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium px-4 py-2 transition-colors"
          >
            + Crear producto
          </button>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            placeholder="Buscar producto por nombre..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
          />
          <select
            value={filtroCategoria}
            onChange={(e) => setFiltroCategoria(e.target.value)}
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
          >
            <option value="todas">Todas las categorías</option>
            {categorias.map((cat) => (
              <option key={cat.categoria_id} value={cat.categoria_id}>
                {cat.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
          {loading && (
            <p className="text-sm text-slate-400 px-5 py-6">
              Cargando productos...
            </p>
          )}

          {!loading && error && (
            <p className="text-sm text-red-600 px-5 py-6">
              No se pudieron cargar los productos: {error}
            </p>
          )}

          {!loading && !error && (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 text-left text-xs font-medium text-slate-500">
                  <th className="px-5 py-3">Producto</th>
                  <th className="px-5 py-3">Categoría</th>
                  <th className="px-5 py-3">Precio venta</th>
                  <th className="px-5 py-3">Unidad</th>
                  <th className="px-5 py-3">Estado</th>
                  <th className="px-5 py-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {productosFiltrados.map((p) => (
                  <tr key={p.producto_id} className="hover:bg-slate-50">
                    <td className="px-5 py-3">
                      <p className="font-medium text-slate-800">{p.nombre}</p>
                      {p.descripcion && (
                        <p className="text-xs text-slate-400 line-clamp-1">
                          {p.descripcion}
                        </p>
                      )}
                    </td>
                    <td className="px-5 py-3 text-slate-600">
                      {mapaCategorias[p.categoria_id] || "—"}
                    </td>
                    <td className="px-5 py-3 text-slate-800 font-medium">
                      ${Number(p.precio_venta).toFixed(2)}
                    </td>
                    <td className="px-5 py-3 text-slate-600">
                      {p.unidad_medida}
                    </td>
                    <td className="px-5 py-3">
                      <span
                        className={`inline-flex items-center rounded-full text-xs font-medium px-2.5 py-1 ${
                          p.activo
                            ? "bg-emerald-50 text-emerald-700"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {p.activo ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                    <td className="px-5 py-3">
                      <div className="flex justify-end gap-3">
                        <button
                          onClick={() => abrirEditar(p)}
                          className="text-xs font-medium text-indigo-600 hover:text-indigo-800"
                        >
                          Editar
                        </button>
                        {p.activo && (
                          <button
                            onClick={() => handleDesactivar(p)}
                            className="text-xs font-medium text-red-600 hover:text-red-800"
                          >
                            Desactivar
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}

                {productosFiltrados.length === 0 && (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-5 py-8 text-center text-sm text-slate-400"
                    >
                      No hay productos que coincidan con la búsqueda.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {modalAbierto && (
        <ProductoModal
          producto={productoEditando}
          categorias={categorias}
          onClose={() => setModalAbierto(false)}
          onSubmit={handleGuardar}
        />
      )}
    </DashboardLayout>
  );
}
