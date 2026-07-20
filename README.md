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

## Estructura del Proyecto

```
SmartStock/
├── backend/        # API REST con FastAPI (Python)
├── frontend/       # Interfaz de usuario con React (Vite)
└── README.md
```

---

## Tecnologías

### Backend
| Componente | Tecnología |
|------------|------------|
| Framework | FastAPI |
| Base de datos | PostgreSQL |
| ORM | SQLAlchemy |
| Migraciones | Alembic |
| Motor de IA | Groq (Llama 3.3 70B) |
| Gráficas | Matplotlib |
| Autenticación | JWT |

### Frontend
| Componente | Tecnología |
|------------|------------|
| Framework | React 19 |
| Build Tool | Vite 8 |
| HTTP Client | Axios |
| Estilos | Tailwind CSS 4 |
| Gráficas | Recharts |
| Estado | Zustand |

---

## Instalación Rápida

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
# Configurar .env con DATABASE_URL, GROQ_API_KEY, SECRET_KEY
alembic upgrade head
python -m script.seed_admin
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
# Configurar .env con VITE_API_BASE_URL
npm run dev
```

---

## Documentación

| Archivo | Contenido |
|---------|-----------|
| `backend/GUIA_INSTALACION.md` | Guía completa de instalación |
| `backend/DOC_IA.md` | Documentación del módulo de IA |
| `backend/DOC_PROMPTS.md` | Prompts utilizados en la IA |
| `backend/DOC_PROMPT_PYTEST.md` | Prompts para generar pruebas |
| `frontend/README.md` | Documentación del frontend |

---

## Credenciales por Defecto

- **Correo:** admin@smartstock.com
- **Contraseña:** admin123

---

## Autores

- **Andrés Banda** — Backend, base de datos, API REST, IA
- **Nathan Carrasco** — Frontend, interfaz de usuario, integración
