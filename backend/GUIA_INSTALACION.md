# SmartStock — Guía de Instalación y Ejecución

Sistema Inteligente de Gestión de Inventario y Predicción de Demanda para PyMEs de Panamá.

---

## Requisitos Previos

| Software | Versión | Propósito |
|----------|---------|-----------|
| Python | 3.11+ | Backend |
| Node.js | 18+ | Frontend |
| PostgreSQL | 14+ | Base de datos |
| Git | Última versión | Control de versiones |

---

## Estructura del Proyecto

```
SmartStock/
├── Proyecto-Backend-main/      # Backend (FastAPI)
│   ├── app/
│   ├── script/
│   ├── alembic/
│   ├── static/
│   ├── requirements.txt
│   └── .env
│
└── smartstock-frontend/        # Frontend (React)
    ├── src/
    ├── package.json
    └── .env
```

---

## 1. Instalación del Backend

### 1.1 Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Proyecto-Backend-main
```

### 1.2 Crear entorno virtual

```bash
python -m venv venv
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 1.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 1.4 Configurar variables de entorno

Crear archivo `.env` en la raíz del backend:

```env
# Base de datos
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/smartstock_db

# Seguridad
SECRET_KEY=una_clave_generada_con_python
DEBUG=True

# IA (Groq - Gratis)
GROQ_API_KEY=gsk_tu-api-key-de-groq
GROQ_MODEL=llama-3.3-70b-versatile
```

**Generar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Obtener GROQ_API_KEY (Gratis):**
1. Ve a [console.groq.com](https://console.groq.com)
2. Crea una cuenta (sin tarjeta de crédito)
3. Ve a API Keys → Create API Key
4. Copia la key (empieza con `gsk_`)

### 1.5 Crear base de datos

Abrir PostgreSQL (pgAdmin o psql) y crear la base de datos:

```sql
CREATE DATABASE smartstock_db;
```

### 1.6 Aplicar migraciones

```bash
alembic upgrade head
```

### 1.7 Crear usuario administrador

```bash
python -m script.seed_admin
```

Credenciales por defecto:
- **Correo:** admin@smartstock.com
- **Contraseña:** admin123

### 1.8 Generar datos de prueba (opcional)

```bash
python -m script.generar_historial_ventas --dias 180 --yes
```

### 1.9 Ejecutar el backend

```bash
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://127.0.0.1:8000`

Documentación Swagger: `http://127.0.0.1:8000/docs`

---

## 2. Instalación del Frontend

### 2.1 Ir a la carpeta del frontend

```bash
cd smartstock-frontend
```

### 2.2 Instalar dependencias

```bash
npm install
```

### 2.3 Configurar variables de entorno

Crear archivo `.env` en la raíz del frontend:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 2.4 Ejecutar el frontend

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

---

## 3. Ejecutar Ambos al Mismo Tiempo

Abrir **dos terminales**:

**Terminal 1 - Backend:**
```bash
cd Proyecto-Backend-main
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd smartstock-frontend
npm run dev
```

---

## 4. URLs de los Servicios

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| Swagger Docs | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Login | http://localhost:5173/login |
| Predicción IA | http://localhost:5173/prediccion |

---

## 5. Iniciar Sesión

1. Abrir http://localhost:5173/login
2. Ingresar:
   - **Correo:** admin@smartstock.com
   - **Contraseña:** admin123

---

## 6. Módulo de IA - Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/ai/prediccion-demanda` | Predicción de demanda con IA |
| POST | `/api/v1/ai/reporte-ventas` | Reporte ejecutivo + gráficas |
| GET | `/api/v1/ai/grafica/tendencia` | Gráfica de tendencia |
| GET | `/api/v1/ai/grafica/mensuales` | Gráfica de barras mensuales |
| GET | `/api/v1/ai/grafica/categoria` | Gráfica de pastel por categoría |

---

## 7. Solución de Problemas

### Error: "psycopg2.errors.UndefinedTable"
Las tablas no existen. Ejecutar:
```bash
alembic upgrade head
```

### Error: "ModuleNotFoundError: No module named 'script'"
Estás en la carpeta incorrecta. Ejecutar desde el backend:
```bash
cd Proyecto-Backend-main
python -m script.seed_admin
```

### Error: "Error al generar predicción: Function.__init__() got an unexpected keyword argument 'days'"
El backend necesita reiniciarse después de los cambios. Ejecutar:
```bash
uvicorn app.main:app --reload
```

### Error: "No se pudo cargar la predicción"
Verificar que:
1. El backend esté corriendo en `http://127.0.0.1:8000`
2. La API key de Groq esté configurada en `.env`
3. La base de datos tenga datos (ejecutar `generar_historial_ventas`)

### Frontend no conecta con backend
Verificar que el `.env` del frontend tenga:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

## 8. Tecnologías Utilizadas

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| FastAPI | 0.115.6 | API REST |
| PostgreSQL | - | Base de datos |
| SQLAlchemy | 2.0.36 | ORM |
| Alembic | 1.14.0 | Migraciones |
| Pydantic | 2.10.4 | Validación |
| Groq | 0.13.0 | Motor de IA |
| Llama 3.3 | 70B | Modelo de IA |
| Matplotlib | 3.9.3 | Gráficas |
| JWT | python-jose | Autenticación |
| bcrypt | passlib | Cifrado |

### Frontend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| React | 19.2.7 | UI Framework |
| Vite | 8.1.1 | Build tool |
| Axios | 1.18.1 | HTTP Client |
| React Router | 7.18.1 | Navegación |
| Recharts | 3.9.2 | Gráficas |
| Tailwind CSS | 4.3.3 | Estilos |
| Zustand | 5.0.14 | Estado global |
