# SmartStock

Sistema Inteligente de Gestión de Inventario y Predicción de Demanda para PyMEs de Panamá.

---

## Descripción

SmartStock es una aplicación web que combina un backend robusto con FastAPI y un frontend moderno con React para ofrecer:

- Gestión completa de inventario (productos, categorías, proveedores, clientes)
- Registro de ventas y compras con transacciones atómicas
- Predicción de demanda basada en Inteligencia Artificial (Groq + Llama 3.3)
- Reportes ejecutivos con gráficas automáticas (Matplotlib)
- Autenticación JWT segura

---

## Estado del Proyecto

| Componente | Estado |
|------------|--------|
| Backend (FastAPI) | Completado |
| Base de datos (PostgreSQL) | Completado |
| Módulo de IA (Groq + Llama 3.3) | Completado |
| Gráficas (Matplotlib) | Completadas |
| Frontend (React) | Completado |
| Integración Frontend-Backend | Completada |
| Documentación | Completada |

---

## Estructura del Proyecto

```
SmartStock/
├── backend/                    # API REST con FastAPI (Python)
│   ├── app/
│   │   ├── ai/                 # Módulo de IA (predicción, reportes, gráficas)
│   │   ├── api/v1/             # Controllers (endpoints REST)
│   │   ├── core/               # Configuración, base de datos, seguridad
│   │   ├── models/             # Modelos SQLAlchemy (tablas)
│   │   ├── schemas/            # Schemas Pydantic (validación)
│   │   ├── services/           # Lógica de negocio
│   │   ├── repositories/       # Acceso a datos
│   │   └── middlewares/        # Autenticación JWT
│   ├── alembic/                # Migraciones de base de datos
│   ├── script/                 # Scripts utilitarios
│   ├── tests/                  # Pruebas pytest
│   └── requirements.txt        # Dependencias Python
│
├── frontend/                   # Interfaz de usuario con React (Vite)
│   ├── src/
│   │   ├── api/                # Servicios HTTP (axios)
│   │   ├── components/         # Componentes reutilizables
│   │   ├── pages/              # Páginas/rutas
│   │   ├── routes/             # Configuración de rutas
│   │   └── store/              # Estado global (Zustand)
│   └── package.json            # Dependencias Node.js
│
└── README.md
```

---

## Tecnologías

### Backend
| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework | FastAPI | 0.115.6 |
| Base de datos | PostgreSQL | - |
| ORM | SQLAlchemy | 2.0.36 |
| Migraciones | Alembic | 1.14.0 |
| Motor de IA | Groq | 0.13.0 |
| Modelo de IA | Llama 3.3 70B | - |
| Gráficas | Matplotlib | 3.9.3 |
| Autenticación | JWT (python-jose) | 3.3.0 |
| Cifrado | bcrypt (passlib) | 1.7.4 |
| Servidor | Uvicorn | 0.34.0 |

### Frontend
| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework | React | 19.2.7 |
| Build Tool | Vite | 8.1.1 |
| HTTP Client | Axios | 1.18.1 |
| Navegación | React Router | 7.18.1 |
| Estilos | Tailwind CSS | 4.3.3 |
| Gráficas | Recharts | 3.9.2 |
| Estado | Zustand | 5.0.14 |

---

## Instalación

### Requisitos Previos

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Backend

```bash
# 1. Clonar el repositorio
git clone https://github.com/emunozzz/SmartStock.git
cd SmartStock/backend

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env con:
# DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/smartstock_db
# SECRET_KEY=tu_clave_secreta
# GROQ_API_KEY=tu_api_key_de_groq
# GROQ_MODEL=llama-3.3-70b-versatile

# 5. Crear base de datos
# Abrir PostgreSQL y ejecutar:
# CREATE DATABASE smartstock_db;

# 6. Aplicar migraciones
alembic upgrade head

# 7. Crear usuario administrador
python -m script.seed_admin

# 8. Generar datos de prueba (opcional)
python -m script.generar_historial_ventas --dias 180 --yes

# 9. Ejecutar el servidor
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://127.0.0.1:8000`

### Frontend

```bash
# 1. Ir a la carpeta del frontend
cd ../frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
# Crear archivo .env con:
# VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

# 4. Ejecutar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

---

## Endpoints de la API

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Iniciar sesión |

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/productos` | Listar productos |
| POST | `/api/v1/productos` | Crear producto |
| GET | `/api/v1/productos/{id}` | Obtener producto |
| PUT | `/api/v1/productos/{id}` | Actualizar producto |
| DELETE | `/api/v1/productos/{id}` | Eliminar producto (soft delete) |

### Inteligencia Artificial
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/ai/prediccion-demanda` | Predicción de demanda con IA |
| POST | `/api/v1/ai/reporte-ventas` | Reporte ejecutivo + gráficas |
| GET | `/api/v1/ai/grafica/tendencia` | Gráfica de tendencia |
| GET | `/api/v1/ai/grafica/mensuales` | Gráfica de barras mensuales |
| GET | `/api/v1/ai/grafica/categoria` | Gráfica de pastel por categoría |

### Otros Endpoints
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST | `/api/v1/categorias` | Gestión de categorías |
| GET/POST | `/api/v1/proveedores` | Gestión de proveedores |
| GET/POST | `/api/v1/clientes` | Gestión de clientes |
| GET/POST | `/api/v1/inventario` | Consulta de inventario |
| GET/POST | `/api/v1/compras` | Registro de compras |
| GET/POST | `/api/v1/ventas` | Registro de ventas |

---

## Módulo de IA

### Predicción de Demanda
```bash
POST /api/v1/ai/prediccion-demanda
Content-Type: application/json

{
  "dias_historial": 90
}
```

Respuesta:
```json
{
  "insights": {
    "producto_mayor_tendencia": {
      "nombre": "Café Molido 500g",
      "variacion_pct": 18.4
    },
    "producto_riesgo_quiebre": {
      "nombre": "CD Virgen 700MB",
      "dias_restantes_stock": 6
    },
    "precision_modelo_pct": 87.2
  },
  "proyeccion": [
    { "periodo": "Feb", "demanda_historica": 420, "demanda_proyectada": 410 }
  ]
}
```

### Reporte de Ventas
```bash
POST /api/v1/ai/reporte-ventas
Content-Type: application/json

{
  "dias": 30
}
```

Respuesta incluye:
- Resumen ejecutivo
- Productos estrella
- Productos que necesitan atención
- Alertas de reabastecimiento
- Recomendaciones
- URLs de 3 gráficas generadas

---

## Credenciales por Defecto

- **Correo:** admin@smartstock.com
- **Contraseña:** admin123

---

## Documentación Adicional

| Archivo | Contenido |
|---------|-----------|
| `backend/GUIA_INSTALACION.md` | Guía completa de instalación |
| `backend/DOC_IA.md` | Documentación del módulo de IA |
| `backend/DOC_PROMPTS.md` | Prompts utilizados en la IA |
| `backend/DOC_PROMPT_PYTEST.md` | Prompts para generar pruebas con pytest |
| `frontend/README.md` | Documentación del frontend |

---

## Solución de Problemas

### Error: "psycopg2.errors.UndefinedTable"
```bash
alembic upgrade head
```

### Error: "ModuleNotFoundError: No module named 'script'"
```bash
cd SmartStock/backend
python -m script.seed_admin
```

### Error: "Error al generar predicción"
Reiniciar el backend:
```bash
uvicorn app.main:app --reload
```

### Frontend no conecta con backend
Verificar que el `.env` del frontend tenga:
```
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

## Autores

- **Andrés Banda** — Backend, base de datos, API REST, módulo de IA
- **Nathan Carrasco** — Frontend, interfaz de usuario, integración

---

## Licencia

Proyecto universitario SmartStock.
