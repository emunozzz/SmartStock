# Módulo de Inteligencia Artificial — SmartStock

## Descripción

El módulo de IA integra **Groq** (con modelo Llama 3.3) para generar predicciones de demanda y reportes ejecutivos de ventas. También genera gráficas automáticamente con **Matplotlib**.

---

## Tecnologías utilizadas

| Categoría | Tecnología | Versión | Propósito |
|-----------|------------|---------|-----------|
| **Framework Backend** | FastAPI | 0.115.6 | API REST asíncrona |
| **Base de datos** | PostgreSQL | - | Almacenamiento relacional |
| **ORM** | SQLAlchemy | 2.0.36 | Mapeo objeto-relacional |
| **Migraciones** | Alembic | 1.14.0 | Control de versiones de la DB |
| **Validación** | Pydantic | 2.10.4 | Validación de datos y schemas |
| **Motor de IA** | Groq | 0.13.0 | Inferencia de modelos de lenguaje |
| **Modelo de IA** | Llama 3.3 70B | - | Análisis y generación de texto |
| **Gráficas** | Matplotlib | 3.9.3 | Generación de imágenes de datos |
| **Autenticación** | JWT (python-jose) | 3.3.0 | Tokens de acceso |
| **Cifrado** | bcrypt (passlib) | 1.7.4 | Cifrado de contraseñas |
| **Servidor ASGI** | Uvicorn | 0.34.0 | Servidor de producción |
| **Entorno** | Python | 3.11+ | Lenguaje de programación |

### Por qué se eligieron estas tecnologías

- **Groq**: API gratuita, ultra rápida (~1s por respuesta), sin tarjeta de crédito
- **Llama 3.3**: Modelo open-source potente, optimizado para análisis de datos
- **Matplotlib**: Estándar de la industria para gráficas en Python, fácil de usar
- **FastAPI**: Rendimiento alto, documentación automática, validación con Pydantic
- **SQLAlchemy**: ORM robusto, soporte completo para PostgreSQL

---

## Dependencias adicionales

Agregar al `requirements.txt` (ya incluido):

```
groq==0.13.0
matplotlib==3.9.3
```

Instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

### 1. Obtener API Key de Groq (Gratis)

1. Ve a [console.groq.com](https://console.groq.com)
2. Crea una cuenta (no requiere tarjeta de crédito)
3. Ve a **API Keys** → **Create API Key**
4. Copia la key (empieza con `gsk_`)

### 2. Configurar variables de entorno

Agregar al archivo `.env`:

```env
GROQ_API_KEY=gsk_tu-api-key-aqui
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Generar datos de prueba

Para probar el módulo de IA necesitas datos de ventas en la base de datos.

```bash
# Genera 180 días de ventas sintéticas
python -m script.generar_historial_ventas --dias 180 --yes

# Genera con semilla reproducible
python -m script.generar_historial_ventas --dias 365 --semilla 42 --yes

# Borrar el historial generado
python -m script.generar_historial_ventas --reset --yes
```

---

## Endpoints de IA

### Predicción de demanda

```http
POST /api/v1/ai/prediccion-demanda
Content-Type: application/json

{
  "dias_historial": 90
}
```

**Respuesta:**
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
      "recomendacion": "Mantener stock actual..."
    }
  ],
  "resumen_general": "Resumen ejecutivo...",
  "modelo_usado": "llama-3.3-70b-versatile",
  "tokens_utilizados": 725
}
```

### Reporte de ventas

```http
POST /api/v1/ai/reporte-ventas
Content-Type: application/json

{
  "dias": 30
}
```

**Respuesta incluye:**
- Resumen ejecutivo
- Productos estrella
- Productos que necesitan atención
- Alertas de reabastecimiento
- Recomendaciones
- URLs de 3 gráficas generadas

### Gráficas individuales

```http
GET /api/v1/ai/grafica/tendencia?dias=30
GET /api/v1/ai/grafica/mensuales?meses=6
GET /api/v1/ai/grafica/categoria?dias=30
```

Estos endpoints devuelven directamente la imagen PNG.

### Ver gráficas generadas

Las gráficas también se pueden ver directamente en el navegador:

```
http://127.0.0.1:8000/static/graficas/tendencia_ventas_30d.png
http://127.0.0.1:8000/static/graficas/ventas_mensuales.png
http://127.0.0.1:8000/static/graficas/ventas_categoria_30d.png
```

---

## Estructura del módulo

```
app/ai/
├── __init__.py
├── prompt_builder.py      # Construye los prompts para Groq
├── prediccion_service.py  # Llama a Groq para predicciones
├── reporte_service.py     # Llama a Groq para reportes
└── graficas_service.py    # Genera gráficas con Matplotlib
```

---

## Cómo funciona el flujo

```
1. El usuario envía POST /api/v1/ai/reporte-ventas
                          │
2. prompt_builder.py      │ Consulta la DB y arma el prompt
   construye el prompt    │ con ventas, productos, inventario
                          │
3. reporte_service.py     │ Envía el prompt a Groq
   llama a Groq           │ y recibe análisis en JSON
                          │
4. graficas_service.py    │ Genera 3 gráficas PNG
   genera gráficas        │ con Matplotlib
                          │
5. Controller返回          │ Devuelve JSON con análisis
                          │ y URLs de las gráficas
```

---

## Solución de problemas

### Error 500: "Error al generar reporte"
- Verificar que `GROQ_API_KEY` esté configurada en `.env`
- Verificar que la API key sea válida en [console.groq.com](https://console.groq.com)

### Error: "No such file or directory" en gráficas
- Verificar que la carpeta `static/graficas/` exista
- Ejecutar `alembic upgrade head` para crear las tablas

### Error: "psycopg2.errors.UndefinedTable"
- Las tablas no existen en la base de datos
- Ejecutar: `alembic upgrade head`

### No hay datos en las gráficas
- Generar historial de ventas: `python -m script.generar_historial_ventas --dias 180 --yes`

---

## Modelos soportados

El módulo usa **Groq** que soporta varios modelos:

| Modelo | Velocidad | Calidad | Costo |
|--------|-----------|---------|-------|
| `llama-3.3-70b-versatile` | Rápida | Alta | Gratis |
| `llama-3.1-8b-instant` | Muy rápida | Media | Gratis |
| `mixtral-8x7b-32768` | Rápida | Alta | Gratis |

Para cambiar el modelo, modificar `GROQ_MODEL` en `.env`:
```env
GROQ_MODEL=llama-3.1-8b-instant
```
