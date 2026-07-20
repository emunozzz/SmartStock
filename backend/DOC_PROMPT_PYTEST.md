# Prompt para Generar Pruebas Pytest con IA

Copia y pega este prompt en ChatGPT, Groq, o cualquier IA para que te genere pruebas pytest para SmartStock.

---

## Prompt Base

```
Eres un experto en testing con Python. Necesito que me generes pruebas pytest para un proyecto de FastAPI llamado SmartStock.

CONTEXTO DEL PROYECTO:
- Framework: FastAPI
- ORM: SQLAlchemy (PostgreSQL)
- Migraciones: Alembic
- Autenticación: JWT con python-jose + bcrypt
- IA: Groq (Llama 3.3) para predicción de demanda

ESTRUCTURA DEL PROYECTO:
app/
├── ai/
│   ├── prompt_builder.py      # Construye prompts para IA
│   ├── prediccion_service.py  # Llama a Groq para predicciones
│   ├── reporte_service.py     # Llama a Groq para reportes
│   └── graficas_service.py    # Genera gráficas con Matplotlib
├── api/v1/
│   ├── ai_controller.py       # Endpoints de IA
│   ├── auth_controller.py     # Login
│   ├── producto_controller.py # CRUD productos
│   └── venta_controller.py    # CRUD ventas
├── models/
│   ├── producto_model.py
│   ├── venta_model.py
│   └── inventario_model.py
├── schemas/
│   ├── ai_schema.py
│   └── auth_schema.py
├── services/
│   └── auth_service.py
└── core/
    ├── config.py
    ├── database.py
    └── security.py

ARCHIVOS RELEVANTES PARA TESTING:

1. app/ai/prompt_builder.py:
- construir_prompt_prediccion(db, dias_historial) -> str
- construir_prompt_reporte(db, dias) -> str
- Usa SQLAlchemy para consultar productos, ventas, inventario

2. app/schemas/ai_schema.py:
- PrediccionRequest(dias_historial: int)
- PrediccionResponse(insights, proyeccion)
- ReporteRequest(dias: int)
- ReporteResponse(resumen_ejecutivo, productos_estrella, graficas, ...)

3. app/api/v1/ai_controller.py:
- POST /api/v1/ai/prediccion-demanda
- POST /api/v1/ai/reporte-ventas
- GET /api/v1/ai/grafica/tendencia
- GET /api/v1/ai/grafica/mensuales
- GET /api/v1/ai/grafica/categoria

TAREAS QUE NECESITO:

1. Genera pruebas UNITARIAS para:
   - Prompt builder (verificar que genera prompts válidos)
   - Schemas Pydantic (verificar validación)

2. Pruebas con MOCK para:
   - Predicción de IA (sin llamar a Groq real)
   - Reporte de IA (sin llamar a Groq real)

3. Pruebas de ENDPOINTS para:
   - Todos los endpoints de IA
   - Login y autenticación
   - CRUD de productos y ventas

4. Fixtures necesarios:
   - Cliente FastAPI de test
   - Sesión de base de datos de test
   - Datos de prueba (productos, ventas, usuario admin)
   - Token JWT de prueba

FORMATO DE SALIDA:
- Usa pytest
- Usa pytest-asyncio para endpoints async
- Usa unittest.mock para mocks
- Incluye docstrings en cada prueba
- Agrupa por módulo con classes o carpetas
- Incluye conftest.py con fixtures compartidos

EJEMPLO DE PRUEBA ESPERADA:
def test_construir_prompt_prediccion_devuelve_string():
    """Verifica que el prompt builder retorna un string no vacío."""
    # Arrange
    db = get_test_db()
    
    # Act
    prompt = construir_prompt_prediccion(db, dias_historial=30)
    
    # Assert
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "SmartStock" in prompt
```

---

## Prompt de Seguimiento

Si necesitas más pruebas o ajustes, usa este prompt:

```
Continuando con las pruebas de SmartStock, necesito que me generes:

1. Pruebas de ERROR para:
   - Base de datos sin conexión
   - API key de Groq inválida
   - Token JWT expirado
   - Datos de entrada inválidos

2. Pruebas de INTEGRACIÓN para:
   - Flujo completo: crear venta → verificar inventario → generar predicción
   - Login → obtener token → usar endpoint protegido

3. Pruebas de RENDIMIENTO para:
   - Respuesta de endpoints en menos de 2 segundos
   - Generación de gráficas en menos de 5 segundos

4. Pruebas de EDGE CASES para:
   - Producto sin ventas históricas
   - Base de datos vacía
   - Fechas límite (365 días máximos)
   - Números decimales en precios
```

---

## Prompt para Generar conftest.py

```
Necesito un archivo conftest.py completo para pytest con FastAPI. El proyecto tiene:

- FastAPI con routers en app/api/v1/
- SQLAlchemy con PostgreSQL
- JWT para autenticación
- Pydantic para schemas

Requisitos del conftest.py:
1. Fixture para cliente FastAPI (TestClient)
2. Fixture para sesión de BD de test (crear/limpiar tablas)
3. Fixture para usuario admin de prueba
4. Fixture para token JWT válido
5. Fixture para datos de prueba (productos, categorías, ventas)
6. Cleanup automático después de cada prueba
7. Configuración de base de datos de test (no usar la de desarrollo)

La base de datos de test debe:
- Crearse automáticamente
- Limpiarse después de cada prueba
- Cerrarse al finalizar
```

---

## Prompt para Ejecutar Todas las Pruebas

```
Dame el comando para ejecutar todas las pruebas de pytest con:
- Modo verbose
- Cobertura de código
- Reporte HTML
- Solo pruebas del módulo de IA
- Pruebas que fallen primero
```

**Comando esperado:**
```bash
pytest -v --cov=app --cov-report=html --html=report.html -k "ai" --tb=short
```
