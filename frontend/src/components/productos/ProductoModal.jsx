import { useEffect, useState } from "react";

const EMPTY_FORM = {
  nombre: "",
  descripcion: "",
  categoria_id: "",
  precio_compra: "",
  precio_venta: "",
  unidad_medida: "",
};

/**
 * Modal reutilizable para Crear y Editar producto.
 * Si "producto" viene con datos, el formulario entra en modo edición
 * (precarga los campos y el submit dispara onSubmit con esos cambios).
 */
export default function ProductoModal({ producto, categorias, onClose, onSubmit }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const esEdicion = Boolean(producto);

  useEffect(() => {
    if (producto) {
      setForm({
        nombre: producto.nombre ?? "",
        descripcion: producto.descripcion ?? "",
        categoria_id: producto.categoria_id ?? "",
        precio_compra: producto.precio_compra ?? "",
        precio_venta: producto.precio_venta ?? "",
        unidad_medida: producto.unidad_medida ?? "",
      });
    } else {
      setForm(EMPTY_FORM);
    }
  }, [producto]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSaving(true);

    try {
      await onSubmit({
        ...form,
        categoria_id: Number(form.categoria_id),
        precio_compra: String(form.precio_compra),
        precio_venta: String(form.precio_venta),
      });
    } catch (err) {
      setError(err.message || "No se pudo guardar el producto.");
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg">
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
          <h2 className="text-sm font-semibold text-slate-900">
            {esEdicion ? "Editar producto" : "Crear producto"}
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-sm"
            aria-label="Cerrar"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-5 py-4 space-y-3">
          {error && (
            <div className="rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm px-3 py-2">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">
              Nombre
            </label>
            <input
              name="nombre"
              required
              value={form.nombre}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">
              Descripción
            </label>
            <textarea
              name="descripcion"
              rows={2}
              value={form.descripcion}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">
              Categoría
            </label>
            <select
              name="categoria_id"
              required
              value={form.categoria_id}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            >
              <option value="" disabled>
                Selecciona una categoría
              </option>
              {categorias.map((cat) => (
                <option key={cat.categoria_id} value={cat.categoria_id}>
                  {cat.nombre}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">
                Precio compra
              </label>
              <input
                name="precio_compra"
                type="number"
                step="0.01"
                min="0"
                required
                value={form.precio_compra}
                onChange={handleChange}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">
                Precio venta
              </label>
              <input
                name="precio_venta"
                type="number"
                step="0.01"
                min="0"
                required
                value={form.precio_venta}
                onChange={handleChange}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">
              Unidad de medida
            </label>
            <input
              name="unidad_medida"
              placeholder="ej. unidad, caja, kg"
              required
              value={form.unidad_medida}
              onChange={handleChange}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg px-3 py-2 text-sm text-slate-600 hover:bg-slate-100 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={saving}
              className="rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white text-sm font-medium px-4 py-2 transition-colors"
            >
              {saving ? "Guardando..." : esEdicion ? "Guardar cambios" : "Crear producto"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
