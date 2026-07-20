# SmartStock — Backend

Sistema Inteligente de Gestión de Inventario y Predicción de Demanda para PyMEs de Panamá.

API REST desarrollada con **FastAPI**, utilizando **PostgreSQL** como base de datos y **SQLAlchemy** como ORM.

Este backend constituye el núcleo técnico del proyecto, incluyendo la arquitectura, el diseño de la base de datos y la lógica de negocio principal, sobre el cual el resto del equipo integra el frontend, la autenticación y el módulo de predicción de demanda basado en Inteligencia Artificial.

---

# Tecnologías

| Componente | Tecnología |
|------------|------------|
| Framework Backend | FastAPI |
| Base de datos | PostgreSQL |
| ORM | SQLAlchemy |
| Migraciones | Alembic |
| Validación de datos | Pydantic |
| Autenticación | JWT (python-jose) + bcrypt (passlib) |
| Servidor ASGI | Uvicorn |

---

# Arquitectura

Arquitectura **Cliente-Servidor basada en API REST**, organizada en capas.

```text
Frontend (React)
        │
 HTTP / JSON
        │
        ▼
Controllers (app/api/v1)
        │
        ▼
Services (app/services)
        │
        ▼
Repositories (app/repositories)
        │
        ▼
Models (app/models)
        │
        ▼
PostgreSQL
```

### Responsabilidad de cada capa

- **Controllers:** exponen los endpoints REST.
- **Services:** contienen la lógica de negocio.
- **Repositories:** realizan el acceso a datos mediante SQLAlchemy.
- **Models:** representan las tablas de la base de datos.

Cada capa posee una única responsabilidad. Los **Controllers** nunca acceden directamente a la base de datos y los **Repositories** no contienen lógica de negocio.

---

# Estructura del proyecto

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── middlewares/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── api/
│   │   └── v1/
│   ├── ai/
│   └── utils/
├── alembic/
│   └── versions/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

# Módulos implementados

| Módulo | Funcionalidad |
|---------|---------------|
| **Autenticación** | Login mediante JWT (`/api/v1/auth/login`) |
| **Usuarios y Roles** | Gestión de usuarios y roles con contraseñas cifradas mediante bcrypt |
| **Productos** | CRUD completo con eliminación lógica (Soft Delete) |
| **Categorías** | CRUD completo |
| **Proveedores** | CRUD y relación N:M con productos |
| **Clientes** | CRUD e historial de compras |
| **Inventario** | Consulta de stock, movimientos y alertas de inventario |
| **Compras** | Registro de compras y actualización automática del inventario |
| **Ventas** | Registro de ventas con validación y descuento automático de stock |

---

# Requisitos previos

- Python 3.11 o superior
- PostgreSQL
- pgAdmin (recomendado)
- Git

---

# Instalación y configuración

## 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd backend
```

---

## 2. Crear el entorno virtual

```bash
python -m venv venv
```

### Activarlo

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Copiar el archivo de ejemplo:

```bash
cp .env.example .env
```

Configurar el archivo `.env`:

```env
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/smartstock_db
SECRET_KEY=una_clave_generada_de_forma_segura
DEBUG=True
```

Para generar una clave segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 5. Crear la base de datos

Crear una base de datos llamada:

```
smartstock_db
```

Puede hacerse mediante **pgAdmin** o **psql**.

---

## 6. Aplicar las migraciones

```bash
alembic upgrade head
```

Esto creará automáticamente todas las tablas del sistema en PostgreSQL.

---

## 7. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

---

# Documentación de la API

FastAPI genera automáticamente la documentación interactiva.

| Herramienta | URL |
|-------------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

Desde **Swagger UI** es posible probar todos los endpoints de la API y autenticarse mediante JWT utilizando el botón **Authorize**.

---

# Flujo de autenticación

1. Crear un rol.
2. Crear un usuario asociado a ese rol.
3. Iniciar sesión mediante:

```
POST /api/v1/auth/login
```

4. Obtener el `access_token`.

5. Enviar el token en cada petición protegida:

```
Authorization: Bearer <token>
```

---

# Decisiones de diseño

### Eliminación lógica (Soft Delete)

Los productos y proveedores no se eliminan físicamente; únicamente se marcan como inactivos para conservar el historial de compras y ventas.

---

### Inventario sin DELETE

No existe un endpoint para eliminar inventario, ya que el historial de movimientos debe mantenerse íntegro.

---

### Transacciones atómicas

Las operaciones de compras y ventas registran:

- Cabecera
- Detalles
- Actualización del inventario

dentro de una única transacción. Si ocurre algún error, toda la operación se revierte automáticamente.

---

### Historial de precios

El precio unitario almacenado en cada detalle de compra o venta corresponde al valor existente al momento de la transacción y permanece inalterable aunque posteriormente cambie el precio del producto.

---

# Próximas mejoras

- Integración del módulo de Inteligencia Artificial (`app/ai`).
- Autorización por roles más granular.
- Módulo de reportes.
- Pruebas automatizadas.
- Documentación técnica adicional.

---

# Autor

**Andrés Banda**

Proyecto universitario **SmartStock**.

Responsabilidades principales:

- Arquitectura del backend.
- Diseño de la base de datos.
- Implementación de la API REST.
- Lógica de negocio.
- Configuración de PostgreSQL y migraciones con Alembic.