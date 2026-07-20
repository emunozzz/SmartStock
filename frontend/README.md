# SmartStock — Frontend

Interfaz de usuario del Sistema Inteligente de Gestión de Inventario y Predicción de Demanda para PyMEs de Panamá.

Desarrollado con **React 19** y **Vite**, consume la API REST del backend de FastAPI.

---

## Tecnologías

| Componente | Tecnología |
|------------|------------|
| Framework UI | React 19 |
| Build Tool | Vite 8 |
| HTTP Client | Axios |
| Navegación | React Router 7 |
| Gráficas | Recharts |
| Estilos | Tailwind CSS 4 |
| Estado Global | Zustand |

---

## Estructura del proyecto

```
frontend/
├── src/
│   ├── api/                # Servicios HTTP (axios)
│   ├── components/         # Componentes reutilizables
│   ├── pages/              # Páginas/rutas
│   ├── routes/             # Configuración de rutas
│   ├── store/              # Estado global (Zustand)
│   ├── assets/             # Imágenes, fuentes
│   ├── App.jsx             # Componente raíz
│   ├── main.jsx            # Punto de entrada
│   └── index.css           # Estilos globales
├── public/                 # Archivos estáticos
├── .env                    # Variables de entorno
├── package.json            # Dependencias
└── vite.config.js          # Configuración de Vite
```

---

## Requisitos previos

- Node.js 18 o superior
- npm o yarn
- Backend de SmartStock corriendo en `http://127.0.0.1:8000`

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd smartstock-frontend
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar variables de entorno

Crear archivo `.env` en la raíz:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

## Ejecución

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

**Nota:** El backend debe estar corriendo en `http://127.0.0.1:8000` para que el frontend funcione.

---

## Scripts disponibles

| Script | Descripción |
|--------|-------------|
| `npm run dev` | Inicia el servidor de desarrollo |
| `npm run build` | Genera la versión de producción |
| `npm run preview` | Vista previa de la versión de producción |
| `npm run lint` | Verifica el código con ESLint |

---

## Páginas

| Ruta | Página | Descripción |
|------|--------|-------------|
| `/login` | Login | Inicio de sesión |
| `/` | Dashboard | Panel principal |
| `/productos` | Productos | Gestión de productos |
| `/ventas` | Ventas | Registro de ventas |
| `/prediccion` | Predicción IA | Predicción de demanda con IA |

---

## Módulo de IA

El frontend consume los endpoints de IA del backend:

- **Predicción de demanda** → `POST /api/v1/ai/prediccion-demanda`
- **Reporte de ventas** → `POST /api/v1/ai/reporte-ventas`
- **Gráficas** → `GET /api/v1/ai/grafica/{tipo}`

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | URL base del backend | `http://127.0.0.1:8000/api/v1` |

---

## Solución de problemas

### Error: "Network Error" o "Failed to fetch"
- Verificar que el backend esté corriendo en `http://127.0.0.1:8000`
- Verificar que CORS esté configurado en el backend

### Error: "401 Unauthorized"
- La sesión expiró. Iniciar sesión nuevamente
- Verificar que el token JWT sea válido

### Error: "Module not found"
Ejecutar:
```bash
npm install
```

### El frontend no carga
Verificar que Node.js esté instalado:
```bash
node --version
```

---

## Autores

### Nathan Carrasco

Responsabilidades principales:

- Desarrollo de la interfaz del frontend con React y Vite.
- Implementación de las pantallas y la experiencia de usuario.
- Integración del frontend con la API REST del backend.
- Manejo de autenticación y consumo de servicios de la aplicación.
