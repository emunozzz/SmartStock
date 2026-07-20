import axiosClient from "./axiosClient";

/**
 * GET /api/v1/productos/
 * Devuelve el listado completo; el filtrado por texto/categoría se hace
 * en el cliente (ver Productos.jsx) para no depender de query params
 * que el backend podría no soportar todavía.
 */
export async function listarProductos() {
  const { data } = await axiosClient.get("/productos/");
  return data;
}

export async function crearProducto(payload) {
  const { data } = await axiosClient.post("/productos/", payload);
  return data;
}

export async function actualizarProducto(productoId, payload) {
  const { data } = await axiosClient.patch(`/productos/${productoId}`, payload);
  return data;
}

/**
 * DELETE /api/v1/productos/{producto_id}
 * Según el README, esto es un borrado lógico (soft delete): el backend
 * marca "activo: false" en vez de eliminar la fila físicamente.
 */
export async function desactivarProducto(productoId) {
  const { data } = await axiosClient.delete(`/productos/${productoId}`);
  return data;
}
