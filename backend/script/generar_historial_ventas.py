"""
generar_historial_ventas.py — Genera datos históricos de ventas sintéticos
para poder probar (y tener con qué armar el prompt de) el módulo de
predicción de demanda de la Fase 5.

POR QUÉ EXISTE ESTE SCRIPT
---------------------------
El endpoint de predicción de demanda (POST /api/v1/ai/prediccion-demanda)
necesita un historial de ventas real para poder mandarle algo con sentido
al modelo. Como el proyecto recién se está armando, la base de datos de
desarrollo no tiene meses de ventas acumuladas -- así que este script las
simula, con patrones deliberadamente distintos por producto para que la
predicción tenga algo interesante que detectar:

  - Café Molido 500g   -> tendencia CRECIENTE sostenida
  - CD Virgen 700MB     -> tendencia DECRECIENTE (producto en desuso)
  - Cerveza Pack x6     -> fuerte estacionalidad de fin de semana
  - Papel Higiénico 4un -> demanda estable, casi sin variación
  - Detergente Líquido 3L -> picos mensuales (efecto "quincena")
  - Impresora Láser     -> demanda esporádica y baja (pocas ventas al mes)

CÓMO FUNCIONA
-------------
No pasa por la API (sería lentísimo insertar meses de ventas una por una
vía HTTP). Inserta directamente con los modelos de SQLAlchemy, pero
replica la misma lógica de negocio que venta_service.py:
  1. Crea (o reutiliza) categoría, productos, inventario, un cliente
     genérico y un usuario "sistema" al que se le atribuyen las ventas.
  2. Por cada día del rango solicitado, decide cuántas ventas hubo y de
     qué productos, según el patrón de cada producto.
  3. Inserta Venta + DetalleVenta con fecha retroactiva (server_default
     de `fecha` se sobreescribe a propósito).
  4. Ajusta inventario.stock_actual y registra el movimiento de salida
     correspondiente, igual que haría una venta real por la API.

Los registros que crea este script quedan marcados (usuario "Sistema —
Datos Históricos IA", categoría "Historial Demo IA") para poder
identificarlos y borrarlos con --reset sin tocar datos reales del resto
del proyecto.

USO
---
    python -m scripts.generar_historial_ventas                 # 180 días, semilla aleatoria
    python -m scripts.generar_historial_ventas --dias 365
    python -m scripts.generar_historial_ventas --semilla 42     # reproducible
    python -m scripts.generar_historial_ventas --reset          # borra el historial generado antes y sale
    python -m scripts.generar_historial_ventas --yes            # sin pedir confirmación

Se ejecuta desde la raíz del proyecto, con el venv activado, y usa la
misma DATABASE_URL del .env que usa la app (por defecto, la base de
DESARROLLO -- no la de test).
"""
import argparse
import random
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from app.core.database import SessionLocal
from app.core.security import hashear_contrasena
from app.models.categoria_model import Categoria
from app.models.cliente_model import Cliente
from app.models.detalle_venta_model import DetalleVenta
from app.models.inventario_model import Inventario
from app.models.movimiento_model import MovimientoInventario
from app.models.producto_model import Producto
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario
from app.models.venta_model import Venta

CATEGORIA_MARCA = "Historial Demo IA"
USUARIO_MARCA_CORREO = "sistema.historial@smartstock.local"
ROL_MARCA = "sistema_historial"
CLIENTE_MARCA = "Cliente Mostrador (historial demo)"

# --- Definición de productos y su patrón de demanda ---
# base: ventas promedio por día "normal"
# tendencia: variación acumulada por día (positiva = crece, negativa = decrece)
# fin_de_semana: multiplicador sáb/dom sobre la base
# quincena: si True, hay picos los días 1, 15 y 30 del mes
# ruido: desviación aleatoria +/- sobre la cantidad final
PRODUCTOS_DEMO = [
    {
        "nombre": "Café Molido 500g", "categoria": "Alimentos",
        "precio_compra": 3.20, "precio_venta": 5.50, "unidad_medida": "unidad",
        "base": 4.0, "tendencia": 0.02, "fin_de_semana": 1.1, "quincena": False, "ruido": 1.5,
    },
    {
        "nombre": "CD Virgen 700MB (pack x10)", "categoria": "Electrónica",
        "precio_compra": 1.80, "precio_venta": 3.00, "unidad_medida": "paquete",
        "base": 3.0, "tendencia": -0.025, "fin_de_semana": 1.0, "quincena": False, "ruido": 1.0,
    },
    {
        "nombre": "Cerveza Pack x6 330ml", "categoria": "Bebidas",
        "precio_compra": 4.50, "precio_venta": 7.00, "unidad_medida": "paquete",
        "base": 3.0, "tendencia": 0.0, "fin_de_semana": 3.2, "quincena": False, "ruido": 2.0,
    },
    {
        "nombre": "Papel Higiénico 4un", "categoria": "Limpieza",
        "precio_compra": 2.00, "precio_venta": 3.20, "unidad_medida": "paquete",
        "base": 6.0, "tendencia": 0.0, "fin_de_semana": 1.05, "quincena": False, "ruido": 1.2,
    },
    {
        "nombre": "Detergente Líquido 3L", "categoria": "Limpieza",
        "precio_compra": 5.00, "precio_venta": 8.50, "unidad_medida": "unidad",
        "base": 2.0, "tendencia": 0.0, "fin_de_semana": 1.0, "quincena": True, "ruido": 1.0,
    },
    {
        "nombre": "Impresora Láser Monocromo", "categoria": "Electrónica",
        "precio_compra": 85.00, "precio_venta": 130.00, "unidad_medida": "unidad",
        "base": 0.15, "tendencia": 0.0, "fin_de_semana": 1.0, "quincena": False, "ruido": 0.4,
    },
]


def obtener_o_crear_categoria(db, nombre: str) -> Categoria:
    categoria = db.query(Categoria).filter(Categoria.nombre == nombre).first()
    if categoria:
        return categoria
    categoria = Categoria(nombre=nombre, descripcion=f"Categoría de demo — {CATEGORIA_MARCA}")
    db.add(categoria)
    db.flush()
    return categoria


def obtener_o_crear_usuario_sistema(db) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.correo == USUARIO_MARCA_CORREO).first()
    if usuario:
        return usuario

    rol = db.query(Rol).filter(Rol.nombre == ROL_MARCA).first()
    if not rol:
        rol = Rol(nombre=ROL_MARCA, descripcion="Rol técnico para atribuir ventas generadas por script")
        db.add(rol)
        db.flush()

    usuario = Usuario(
        nombre="Sistema — Datos Históricos IA",
        correo=USUARIO_MARCA_CORREO,
        contrasena_hash=hashear_contrasena("no-se-usa-para-login-123!"),
        rol_id=rol.rol_id,
    )
    db.add(usuario)
    db.flush()
    return usuario


def obtener_o_crear_cliente(db) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.nombre == CLIENTE_MARCA).first()
    if cliente:
        return cliente
    cliente = Cliente(nombre=CLIENTE_MARCA)
    db.add(cliente)
    db.flush()
    return cliente


def obtener_o_crear_productos(db) -> list[Producto]:
    productos = []
    for defn in PRODUCTOS_DEMO:
        categoria = obtener_o_crear_categoria(db, defn["categoria"])
        producto = db.query(Producto).filter(Producto.nombre == defn["nombre"]).first()
        if not producto:
            producto = Producto(
                nombre=defn["nombre"],
                descripcion=f"Producto de demo — {CATEGORIA_MARCA}",
                categoria_id=categoria.categoria_id,
                precio_compra=Decimal(str(defn["precio_compra"])),
                precio_venta=Decimal(str(defn["precio_venta"])),
                unidad_medida=defn["unidad_medida"],
            )
            db.add(producto)
            db.flush()

        inventario = db.query(Inventario).filter(Inventario.producto_id == producto.producto_id).first()
        if not inventario:
            inventario = Inventario(producto_id=producto.producto_id, stock_actual=100000, stock_minimo=10)
            db.add(inventario)
            db.flush()

        producto._patron = defn  # se adjunta el patrón de demanda para usarlo al generar
        productos.append(producto)
    return productos


def cantidad_del_dia(patron: dict, dia_index: int, fecha: datetime) -> int:
    """Calcula cuántas unidades se vendieron de un producto en un día dado,
    combinando base + tendencia + estacionalidad + ruido."""
    cantidad = patron["base"] + patron["tendencia"] * dia_index

    if fecha.weekday() >= 5:  # sábado=5, domingo=6
        cantidad *= patron["fin_de_semana"]

    if patron["quincena"] and fecha.day in (1, 15, 30):
        cantidad *= 2.5

    cantidad += random.uniform(-patron["ruido"], patron["ruido"])
    return max(0, round(cantidad))


def generar_historial(db, productos: list[Producto], usuario: Usuario, cliente: Cliente, dias: int):
    hoy = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    inicio = hoy - timedelta(days=dias)

    total_ventas = 0
    total_unidades = 0

    for dia_index in range(dias):
        fecha_dia = inicio + timedelta(days=dia_index)

        for producto in productos:
            cantidad = cantidad_del_dia(producto._patron, dia_index, fecha_dia)
            if cantidad <= 0:
                continue

            # cada "venta" del día para este producto es un ticket independiente,
            # con una hora aleatoria dentro del horario comercial (8am-9pm)
            hora = random.randint(8, 20)
            minuto = random.randint(0, 59)
            fecha_venta = fecha_dia.replace(hour=hora, minute=minuto)

            precio_unitario = producto.precio_venta
            subtotal = precio_unitario * cantidad

            venta = Venta(
                cliente_id=cliente.cliente_id,
                usuario_id=usuario.usuario_id,
                fecha=fecha_venta,
                total=subtotal,
                estado="completada",
            )
            db.add(venta)
            db.flush()

            detalle = DetalleVenta(
                venta_id=venta.venta_id,
                producto_id=producto.producto_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )
            db.add(detalle)

            inventario = db.query(Inventario).filter(
                Inventario.producto_id == producto.producto_id
            ).first()
            inventario.stock_actual -= cantidad

            movimiento = MovimientoInventario(
                producto_id=producto.producto_id,
                tipo_movimiento="salida",
                cantidad=cantidad,
                motivo="Venta a cliente (historial generado)",
                referencia_tipo="venta",
                referencia_id=venta.venta_id,
                usuario_id=usuario.usuario_id,
                fecha=fecha_venta,
            )
            db.add(movimiento)

            total_ventas += 1
            total_unidades += cantidad

        if dia_index % 30 == 0:
            db.commit()  # commits parciales: si algo falla a mitad de camino, no se pierde todo
            print(f"  ... día {dia_index}/{dias} ({fecha_dia.date()}) — {total_ventas} ventas generadas hasta ahora")

    db.commit()
    return total_ventas, total_unidades


def reset_historial(db):
    """Borra únicamente los datos marcados como generados por este script,
    sin tocar nada más del proyecto."""
    usuario = db.query(Usuario).filter(Usuario.correo == USUARIO_MARCA_CORREO).first()
    if not usuario:
        print("No hay historial generado por este script para borrar.")
        return

    ventas = db.query(Venta).filter(Venta.usuario_id == usuario.usuario_id).all()
    venta_ids = [v.venta_id for v in ventas]
    print(f"Borrando {len(venta_ids)} ventas (y sus detalles) generadas por el script...")

    db.query(DetalleVenta).filter(DetalleVenta.venta_id.in_(venta_ids)).delete(synchronize_session=False)
    db.query(MovimientoInventario).filter(MovimientoInventario.usuario_id == usuario.usuario_id).delete(synchronize_session=False)
    db.query(Venta).filter(Venta.usuario_id == usuario.usuario_id).delete(synchronize_session=False)
    db.commit()
    print("Historial borrado. Los productos, categorías, inventario y el usuario/cliente de marca NO se tocaron.")


def main():
    parser = argparse.ArgumentParser(description="Genera historial de ventas sintético para probar el módulo de IA.")
    parser.add_argument("--dias", type=int, default=180, help="Cantidad de días de historial hacia atrás (default: 180)")
    parser.add_argument("--semilla", type=int, default=None, help="Semilla para reproducibilidad (default: aleatoria)")
    parser.add_argument("--reset", action="store_true", help="Borra el historial generado previamente y sale, sin generar nada nuevo")
    parser.add_argument("--yes", action="store_true", help="No pedir confirmación antes de escribir en la base de datos")
    args = parser.parse_args()

    if args.semilla is not None:
        random.seed(args.semilla)

    db = SessionLocal()
    try:
        from app.core.config import settings
        print(f"Base de datos destino: {settings.DATABASE_URL}")

        if args.reset:
            if not args.yes and input("¿Confirmas borrar el historial generado por este script? (s/n): ").lower() != "s":
                print("Cancelado.")
                return
            reset_historial(db)
            return

        if not args.yes:
            confirmacion = input(
                f"Se van a insertar ~{args.dias} días de ventas sintéticas en la base de arriba. "
                f"¿Continuar? (s/n): "
            )
            if confirmacion.lower() != "s":
                print("Cancelado.")
                return

        print("Creando/verificando productos, categorías, inventario, cliente y usuario de sistema...")
        usuario = obtener_o_crear_usuario_sistema(db)
        cliente = obtener_o_crear_cliente(db)
        productos = obtener_o_crear_productos(db)
        db.commit()
        print(f"  {len(productos)} productos listos: {', '.join(p.nombre for p in productos)}")

        print(f"Generando {args.dias} días de historial de ventas...")
        total_ventas, total_unidades = generar_historial(db, productos, usuario, cliente, args.dias)

        print(f"\nListo. Se generaron {total_ventas} ventas ({total_unidades} unidades vendidas en total)"
              f" a lo largo de {args.dias} días.")
        print("Para borrar este historial más adelante: python -m scripts.generar_historial_ventas --reset")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
