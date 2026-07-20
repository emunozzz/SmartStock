# Documentación de Prompts — Módulo de IA

Este documento describe los prompts utilizados en el módulo de Inteligencia Artificial de SmartStock.

---

## Resumen

| Prompt | Endpoint | Modelo | Propósito |
|--------|----------|--------|-----------|
| Predicción de demanda | `POST /api/v1/ai/prediccion-demanda` | Llama 3.3 70B | Predecir demanda futura |
| Reporte de ventas | `POST /api/v1/ai/reporte-ventas` | Llama 3.3 70B | Generar reporte ejecutivo |

---

## 1. Prompt de Predicción de Demanda

### Ubicación del código
`app/ai/prompt_builder.py` → función `construir_prompt_prediccion()`

### Endpoint
```
POST /api/v1/ai/prediccion-demanda
Body: { "dias_historial": 90 }
```

### System Message
```
Eres un analista de inventario experto. Respondes siempre en JSON válido, sin texto adicional.
```

### Prompt enviado

```
Eres un analista de inventario para una PyME de Panamá llamada SmartStock.
Tu tarea es analizar el historial de ventas de los productos y generar predicciones de demanda.

CONTEXTO:
- Se te proporciona el historial de ventas de los últimos 90 días.
- Cada producto incluye su nombre, categoría, precio, stock actual y historial diario de unidades vendidas.

PRODUCTOS:
- Café Molido 500g (Alimentos) — $5.5
  Stock actual: 95000, Mínimo: 10
  Últimos días: 2026-07-01: 5u, 2026-07-02: 4u, ...

- CD Virgen 700MB (Electrónica) — $3.0
  Stock actual: 98000, Mínimo: 10
  Últimos días: 2026-07-01: 3u, 2026-07-02: 2u, ...

INSTRUCCIONES:
1. Analiza las tendencias de cada producto (creciente, decreciente, estable, estacional).
2. Identifica patrones por día de semana o fechas especiales.
3. Predice la demanda para los próximos 7 y 30 días.
4. Genera alertas de reabastecimiento si el stock actual es insuficiente.
5. Responde en español, en formato JSON estructurado.

RESPUESTA ESPERADA (JSON):
{
  "predicciones": [
    {
      "producto": "nombre del producto",
      "tendencia": "creciente|decreciente|estable|estacional",
      "demanda_7_dias": número estimado de unidades,
      "demanda_30_dias": número estimado de unidades,
      "alerta_reabastecimiento": true/false,
      "nivel_urgencia": "bajo|medio|alto",
      "recomendacion": "texto con recomendación específica"
    }
  ],
  "resumen_general": "resumen ejecutivo de la situación del inventario"
}

IMPORTANTE: Responde SOLAMENTE con el JSON, sin texto adicional antes o después.
```

### Parámetros de configuración
```python
model = "llama-3.3-70b-versatile"
temperature = 0.3      # Respuestas más precisas y menos creativas
max_tokens = 2000      # Suficiente para respuesta completa
```

### Datos de entrada
El prompt se construye dinámicamente consultando la base de datos:
- **Productos activos** de la tabla `productos`
- **Historial de ventas** de los últimos N días (por defecto 90)
- **Stock actual** de la tabla `inventario`
- **Categoría** de cada producto

### Datos de salida esperados
```json
{
  "predicciones": [
    {
      "producto": "Café Molido 500g",
      "tendencia": "creciente",
      "demanda_7_dias": 35,
      "demanda_30_dias": 150,
      "alerta_reabastecimiento": false,
      "nivel_urgencia": "bajo",
      "recomendacion": "Mantener stock actual, tendencia al alza"
    }
  ],
  "resumen_general": "Los productos muestran tendencia mixta..."
}
```

---

## 2. Prompt de Reporte de Ventas

### Ubicación del código
`app/ai/prompt_builder.py` → función `construir_prompt_reporte()`

### Endpoint
```
POST /api/v1/ai/reporte-ventas
Body: { "dias": 30 }
```

### System Message
```
Eres un analista financiero y de inventario experto. Respondes siempre en JSON válido, sin texto adicional.
```

### Prompt enviado

```
Eres un analista financiero y de inventario para una PyME de Panamá llamada SmartStock.
Genera un reporte ejecutivo de ventas de los últimos 30 días.

DATOS DEL PERÍODO:
- Total de ventas realizadas: 150
- Ingresos totales: $45,230.00

VENTAS POR PRODUCTO (ordenado de mayor a menor):
- Café Molido 500g: 85 unidades, $467.50 en ingresos
- Papel Higiénico 4un: 120 unidades, $384.00 en ingresos
- Cerveza Pack x6: 45 unidades, $315.00 en ingresos

PRODUCTOS CON STOCK BAJO MÍNIMO:
- CD Virgen 700MB: stock actual 5, mínimo 10

INSTRUCCIONES:
1. Resume los resultados del período (ventas, ingresos, tendencias).
2. Identifica los productos estrella y los que necesitan atención.
3. Analiza si hay productos con bajo rendimiento.
4. Genera alertas de reabastecimiento para productos con stock crítico.
5. Da recomendaciones accionables para el próximo mes.
6. Responde en español, en formato JSON estructurado.

RESPUESTA ESPERADA (JSON):
{
  "resumen_ejecutivo": "resumen de 2-3 líneas sobre el desempeño del período",
  "productos_estrella": [
    { "nombre": "producto", "ventas": número, "ingresos": número }
  ],
  "productos_atencion": [
    { "nombre": "producto", "razón": "por qué necesita atención" }
  ],
  "alertas_reabastecimiento": [
    { "producto": "nombre", "stock_actual": número, "stock_minimo": número, "urgencia": "baja|media|alta" }
  ],
  "recomendaciones": [
    "recomendación 1",
    "recomendación 2"
  ],
  "tendencia_general": "positiva|negativa|estable",
  "proyeccion_siguiente_mes": "proyección breve"
}

IMPORTANTE: Responde SOLAMENTE con el JSON, sin texto adicional antes o después.
```

### Parámetros de configuración
```python
model = "llama-3.3-70b-versatile"
temperature = 0.3
max_tokens = 2000
```

### Datos de entrada
El prompt se construye dinámicamente consultando:
- **Total de ventas** del período
- **Ingresos totales** del período
- **Ventas por producto** (ordenado de mayor a menor)
- **Productos con stock bajo** el mínimo

### Datos de salida esperados
```json
{
  "resumen_ejecutivo": "En el último mes, SmartStock generó $45,230 en ingresos...",
  "productos_estrella": [
    { "nombre": "Papel Higiénico 4un", "ventas": 120, "ingresos": 384.00 }
  ],
  "productos_atencion": [
    { "nombre": "CD Virgen 700MB", "razón": "Stock por debajo del mínimo" }
  ],
  "alertas_reabastecimiento": [
    { "producto": "CD Virgen 700MB", "stock_actual": 5, "stock_minimo": 10, "urgencia": "alta" }
  ],
  "recomendaciones": [
    "Reabastecer CD Virgen 700MB urgente",
    "Incrementar promociones de Café Molido"
  ],
  "tendencia_general": "positiva",
  "proyeccion_siguiente_mes": "Se espera un aumento del 10% en ventas"
}
```

---

## 3. Consideraciones de Diseño

### Por qué se usa JSON como formato de salida
- Fácil de parsear en el backend
- Se mapea directamente a schemas de Pydantic
- El frontend puede consumirlo sin transformaciones

### Por qué temperature = 0.3
- Respuestas más consistentes y predecibles
- Menos "alucinaciones" de la IA
- Datos numéricos más precisos

### Por qué Llama 3.3 70B
- Gratuito a través de Groq
- Rápido (~1 segundo por respuesta)
- Buen razonamiento para análisis de datos
- Soporta español correctamente

### Validación de respuestas
El backend valida las respuestas de la IA con Pydantic:
- Si la IA responde con campos faltantes → usa valores por defecto
- Si la IA responde con JSON inválido → retorna respuesta cruda
- Si la IA responde con campos extras → los ignora

---

## 4. Flujo Completo

```
1. Frontend envía POST /api/v1/ai/prediccion-demanda
                          │
2. Controller recibe     │ Extrae dias_historial del body
   la petición           │
                          │
3. Servicio consulta     │ SELECT ventas, productos, inventario
   la base de datos      │ de los últimos N días
                          │
4. Prompt Builder        │ Construye el prompt con los datos
   arma el prompt        │ reales de la BD
                          │
5. Servicio de IA        │ Envía prompt a Groq (Llama 3.3)
   llama a Groq          │ Recibe respuesta en JSON
                          │
6. Servicio transforma   │ Convierte la respuesta al formato
   la respuesta          │ que espera el frontend
                          │
7. Controller retorna    │ Devuelve JSON con insights
   la respuesta          │ y proyección al frontend
                          │
8. Frontend renderiza    │ Muestra gráficas y datos
   los datos             │ en la interfaz
```

---

## 5. Personalización de Prompts

### Cambiar el modelo
En `.env`:
```env
GROQ_MODEL=llama-3.1-8b-instant  # Más rápido, menos preciso
GROQ_MODEL=llama-3.3-70b-versatile  # Más preciso, predeterminado
GROQ_MODEL=mixtral-8x7b-32768  # Alternativa
```

### Ajustar la temperatura
En `prediccion_service.py` o `reporte_service.py`:
```python
temperature=0.1  # Más preciso y conservador
temperature=0.3  # Equilibrado (predeterminado)
temperature=0.7  # Más creativo
```

### Agregar más contexto al prompt
Modificar `construir_prompt_prediccion()` o `construir_prompt_reporte()` en `prompt_builder.py`.
