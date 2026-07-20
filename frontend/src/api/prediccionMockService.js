/**
 * Mock del contrato de la futura API de IA (módulo en desarrollo por el
 * Integrante 2). Cuando el endpoint real exista, esta función se reemplaza
 * por una llamada a axiosClient sin tocar el componente que la consume,
 * siempre que la forma de la respuesta se mantenga igual.
 *
 * Contrato esperado (propuesto):
 * GET /api/v1/ai/prediccion-demanda
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
export async function getPrediccionDemanda() {
  await new Promise((resolve) => setTimeout(resolve, 400)); // simula latencia de red

  return {
    insights: {
      producto_mayor_tendencia: {
        nombre: "Arroz Superior 1lb",
        variacion_pct: 18.4,
      },
      producto_riesgo_quiebre: {
        nombre: "Aceite Vegetal 1L",
        dias_restantes_stock: 6,
      },
      precision_modelo_pct: 87.2,
    },
    proyeccion: [
      { periodo: "Feb", demanda_historica: 420, demanda_proyectada: 410 },
      { periodo: "Mar", demanda_historica: 455, demanda_proyectada: 448 },
      { periodo: "Abr", demanda_historica: 401, demanda_proyectada: 415 },
      { periodo: "May", demanda_historica: 468, demanda_proyectada: 470 },
      { periodo: "Jun", demanda_historica: 512, demanda_proyectada: 505 },
      { periodo: "Jul", demanda_historica: null, demanda_proyectada: 540 },
      { periodo: "Ago", demanda_historica: null, demanda_proyectada: 561 },
      { periodo: "Sep", demanda_historica: null, demanda_proyectada: 578 },
    ],
  };
}
