import axiosClient from "./axiosClient";

/**
 * Servicio real de predicción de demanda.
 * Conecta con el backend de SmartStock usando Groq + Llama 3.3.
 *
 * Contrato:
 * POST /api/v1/ai/prediccion-demanda
 * Body: { "dias_historial": 90 }
 *
 * Respuesta:
 * {
 *   insights: {
 *     producto_mayor_tendencia: { nombre, variacion_pct },
 *     producto_riesgo_quiebre: { nombre, dias_restantes_stock },
 *     precision_modelo_pct: number
 *   },
 *   proyeccion: [
 *     { periodo: "Ene", demanda_historica: number, demanda_proyectada: number }
 *   ]
 * }
 */
export async function getPrediccionDemanda(diasHistorial = 90) {
  const { data } = await axiosClient.post("/ai/prediccion-demanda", {
    dias_historial: diasHistorial,
  });
  return data;
}
