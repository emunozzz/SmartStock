import os
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.detalle_venta_model import DetalleVenta
from app.models.producto_model import Producto
from app.models.categoria_model import Categoria
from app.models.venta_model import Venta

GRAFICAS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "static", "graficas")


def _asegurar_directorio():
    os.makedirs(GRAFICAS_DIR, exist_ok=True)


def _obtener_ventas_por_producto(db: Session, dias: int) -> dict:
    inicio = datetime.now(timezone.utc) - timedelta(days=dias)

    datos = (
        db.query(
            Producto.nombre,
            func.date(Venta.fecha).label("dia"),
            func.sum(DetalleVenta.cantidad).label("total"),
        )
        .select_from(Venta)
        .join(DetalleVenta, DetalleVenta.venta_id == Venta.venta_id)
        .join(Producto, Producto.producto_id == DetalleVenta.producto_id)
        .filter(
            Venta.estado == "completada",
            Venta.fecha >= inicio,
        )
        .group_by(Producto.nombre, func.date(Venta.fecha))
        .order_by(func.date(Venta.fecha))
        .all()
    )

    resultado = {}
    for nombre, dia, total in datos:
        if nombre not in resultado:
            resultado[nombre] = {"dias": [], "unidades": []}
        resultado[nombre]["dias"].append(dia)
        resultado[nombre]["unidades"].append(int(total))

    return resultado


def _obtener_ventas_mensuales(db: Session, meses: int = 6) -> dict:
    inicio = datetime.now(timezone.utc) - timedelta(days=meses * 30)

    datos = (
        db.query(
            func.date_trunc("month", Venta.fecha).label("mes"),
            func.sum(DetalleVenta.cantidad).label("total"),
        )
        .select_from(Venta)
        .join(DetalleVenta, DetalleVenta.venta_id == Venta.venta_id)
        .filter(
            Venta.estado == "completada",
            Venta.fecha >= inicio,
        )
        .group_by(func.date_trunc("month", Venta.fecha))
        .order_by(func.date_trunc("month", Venta.fecha))
        .all()
    )

    meses_labels = [str(mes.strftime("%b %Y")) for mes, _ in datos]
    totales = [int(total) for _, total in datos]

    return {"meses": meses_labels, "totales": totales}


def _obtener_ventas_por_categoria(db: Session, dias: int) -> dict:
    inicio = datetime.now(timezone.utc) - timedelta(days=dias)

    datos = (
        db.query(
            Categoria.nombre,
            func.sum(DetalleVenta.cantidad).label("total"),
        )
        .select_from(Venta)
        .join(DetalleVenta, DetalleVenta.venta_id == Venta.venta_id)
        .join(Producto, Producto.producto_id == DetalleVenta.producto_id)
        .join(Categoria, Categoria.categoria_id == Producto.categoria_id)
        .filter(
            Venta.estado == "completada",
            Venta.fecha >= inicio,
        )
        .group_by(Categoria.nombre)
        .all()
    )

    categorias = [cat for cat, _ in datos]
    totales = [int(total) for _, total in datos]

    return {"categorias": categorias, "totales": totales}


def grafica_tendencia_ventas(db: Session, dias: int = 30) -> str:
    _asegurar_directorio()

    datos = _obtener_ventas_por_producto(db, dias)

    fig, ax = plt.subplots(figsize=(12, 6))

    for nombre, info in datos.items():
        ax.plot(info["dias"], info["unidades"], marker="o", label=nombre, linewidth=2)

    ax.set_title(f"Tendencia de Ventas - Últimos {dias} días", fontsize=14, fontweight="bold")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Unidades Vendidas")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, dias // 10)))
    plt.xticks(rotation=45)
    plt.tight_layout()

    nombre_archivo = f"tendencia_ventas_{dias}d.png"
    ruta = os.path.join(GRAFICAS_DIR, nombre_archivo)
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return ruta


def grafica_ventas_mensuales(db: Session, meses: int = 6) -> str:
    _asegurar_directorio()

    datos = _obtener_ventas_mensuales(db, meses)

    fig, ax = plt.subplots(figsize=(10, 6))

    colores = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]
    barras = ax.bar(datos["meses"], datos["totales"], color=colores[: len(datos["meses"])])

    for barra, total in zip(barras, datos["totales"]):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 5,
            str(total),
            ha="center",
            fontweight="bold",
        )

    ax.set_title("Ventas Mensuales", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Unidades Vendidas")
    ax.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    nombre_archivo = "ventas_mensuales.png"
    ruta = os.path.join(GRAFICAS_DIR, nombre_archivo)
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return ruta


def grafica_ventas_por_categoria(db: Session, dias: int = 30) -> str:
    _asegurar_directorio()

    datos = _obtener_ventas_por_categoria(db, dias)

    fig, ax = plt.subplots(figsize=(8, 8))

    colores = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4", "#FF5722"]
    wedges, texts, autotexts = ax.pie(
        datos["totales"],
        labels=datos["categorias"],
        autopct="%1.1f%%",
        colors=colores[: len(datos["categorias"])],
        startangle=90,
    )

    for text in autotexts:
        text.set_fontweight("bold")

    ax.set_title("Distribución de Ventas por Categoría", fontsize=14, fontweight="bold")
    plt.tight_layout()

    nombre_archivo = f"ventas_categoria_{dias}d.png"
    ruta = os.path.join(GRAFICAS_DIR, nombre_archivo)
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return ruta


def generar_todas_las_graficas(db: Session, dias: int = 30) -> list[str]:
    rutas = []
    rutas.append(grafica_tendencia_ventas(db, dias))
    rutas.append(grafica_ventas_mensuales(db))
    rutas.append(grafica_ventas_por_categoria(db, dias))
    return rutas
