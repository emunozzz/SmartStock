import axiosClient from "./axiosClient";

/**
 * GET /api/v1/inventario/alertas
 * Ajusta la ruta exacta al endpoint dedicado que exponga tu backend
 * (README menciona "alertas de inventario" dentro del módulo Inventario).
 * Se espera una respuesta tipo:
 * [
 *   { producto_id, nombre, stock_actual, stock_minimo, unidad_medida }
 * ]
 */
export async function getAlertasStockBajo() {
  const { data } = await axiosClient.get("/inventario/alertas");
  return data;
}
