from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.detalle_venta_model import DetalleVenta
from app.models.producto_model import Producto
from app.models.venta_model import Venta
from app.models.inventario_model import Inventario


def construir_prompt_prediccion(db: Session, dias_historial: int = 90) -> str:
    productos = db.query(Producto).filter(Producto.activo == True).all()
    fecha_inicio = datetime.now(timezone.utc) - timedelta(days=dias_historial)

    datos_productos = []
    for producto in productos:
        ventas_por_dia = (
            db.query(
                func.date(Venta.fecha).label("dia"),
                func.sum(DetalleVenta.cantidad).label("total_vendido"),
            )
            .select_from(DetalleVenta)
            .join(Venta, DetalleVenta.venta_id == Venta.venta_id)
            .filter(
                DetalleVenta.producto_id == producto.producto_id,
                Venta.estado == "completada",
                Venta.fecha >= fecha_inicio,
            )
            .group_by(func.date(Venta.fecha))
            .order_by(func.date(Venta.fecha))
            .all()
        )

        historial = [
            {"dia": str(v.dia), "unidades": int(v.total_vendido)}
            for v in ventas_por_dia
        ]

        inventario = db.query(Inventario).filter(
            Inventario.producto_id == producto.producto_id
        ).first()

        inventario_data = None
        if inventario:
            inventario_data = {
                "stock_actual": int(inventario.stock_actual),
                "stock_minimo": int(inventario.stock_minimo),
            }

        datos_productos.append({
            "nombre": producto.nombre,
            "categoria": producto.categoria.nombre if producto.categoria else "Sin categoría",
            "precio_venta": float(producto.precio_venta),
            "inventario": inventario_data,
            "historial_ventas": historial,
        })

    prompt = f"""Eres un analista de inventario para una PyME de Panamá llamada SmartStock.
Tu tarea es analizar el historial de ventas de los productos y generar predicciones de demanda.

CONTEXTO:
- Se te proporciona el historial de ventas de los últimos {dias_historial} días.
- Cada producto incluye su nombre, categoría, precio, stock actual y historial diario de unidades vendidas.

PRODUCTOS:
{_formato_productos(datos_productos)}

INSTRUCCIONES:
1. Analiza las tendencias de cada producto (creciente, decreciente, estable, estacional).
2. Identifica patrones por día de semana o fechas especiales.
3. Predice la demanda para los próximos 7 y 30 días.
4. Genera alertas de reabastecimiento si el stock actual es insuficiente.
5. Responde en español, en formato JSON estructurado.

RESPUESTA ESPERADA (JSON):
{{
  "predicciones": [
    {{
      "producto": "nombre del producto",
      "tendencia": "creciente|decreciente|estable|estacional",
      "demanda_7_dias": número estimado de unidades,
      "demanda_30_dias": número estimado de unidades,
      "alerta_reabastecimiento": true/false,
      "nivel_urgencia": "bajo|medio|alto",
      "recomendacion": "texto con recomendación específica"
    }}
  ],
  "resumen_general": "resumen ejecutivo de la situación del inventario"
}}

IMPORTANTE: Responde SOLAMENTE con el JSON, sin texto adicional antes o después."""

    return prompt


def _formato_productos(productos: list[dict]) -> str:
    lineas = []
    for p in productos:
        historial_str = ", ".join(
            [f"{h['dia']}: {h['unidades']}u" for h in p["historial_ventas"][-14:]]
        )
        if not historial_str:
            historial_str = "Sin ventas registradas"

        inv = p["inventario"]
        inv_str = (
            f"Stock actual: {inv['stock_actual']}, Mínimo: {inv['stock_minimo']}"
            if inv
            else "Sin inventario registrado"
        )

        lineas.append(
            f"- {p['nombre']} ({p['categoria']}) — ${p['precio_venta']}\n"
            f"  {inv_str}\n"
            f"  Últimos días: {historial_str}"
        )

    return "\n\n".join(lineas)


def construir_prompt_reporte(db: Session, dias: int = 30) -> str:
    inicio = datetime.now(timezone.utc) - timedelta(days=dias)

    ventas_por_producto = (
        db.query(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad).label("total_vendido"),
            func.sum(DetalleVenta.subtotal).label("total_ingreso"),
        )
        .select_from(DetalleVenta)
        .join(Venta, DetalleVenta.venta_id == Venta.venta_id)
        .join(Producto, Producto.producto_id == DetalleVenta.producto_id)
        .filter(
            Venta.estado == "completada",
            Venta.fecha >= inicio,
        )
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .all()
    )

    productos_texto = []
    for p in ventas_por_producto:
        productos_texto.append(
            f"- {p.nombre}: {int(p.total_vendido)} unidades, ${float(p.total_ingreso):.2f} en ingresos"
        )

    total_ventas = (
        db.query(func.count(Venta.venta_id))
        .filter(Venta.estado == "completada", Venta.fecha >= inicio)
        .scalar()
    )

    total_ingresos = (
        db.query(func.sum(Venta.total))
        .filter(Venta.estado == "completada", Venta.fecha >= inicio)
        .scalar()
    )

    productos_bajo_stock = (
        db.query(Producto.nombre, Inventario.stock_actual, Inventario.stock_minimo)
        .join(Inventario, Inventario.producto_id == Producto.producto_id)
        .filter(Producto.activo == True, Inventario.stock_actual <= Inventario.stock_minimo)
        .all()
    )

    alertas_texto = []
    for p in productos_bajo_stock:
        alertas_texto.append(
            f"- {p.nombre}: stock actual {p.stock_actual}, mínimo {p.stock_minimo}"
        )

    prompt = f"""Eres un analista financiero y de inventario para una PyME de Panamá llamada SmartStock.
Genera un reporte ejecutivo de ventas de los últimos {dias} días.

DATOS DEL PERÍODO:
- Total de ventas realizadas: {total_ventas}
- Ingresos totales: ${float(total_ingresos or 0):.2f}

VENTAS POR PRODUCTO (ordenado de mayor a menor):
{chr(10).join(productos_texto) if productos_texto else "No hay ventas registradas"}

PRODUCTOS CON STOCK BAJO MÍNIMO:
{chr(10).join(alertas_texto) if alertas_texto else "No hay productos con stock bajo"}

INSTRUCCIONES:
1. Resume los resultados del período (ventas, ingresos, tendencias).
2. Identifica los productos estrella y los que necesitan atención.
3. Analiza si hay productos con bajo rendimiento.
4. Genera alertas de reabastecimiento para productos con stock crítico.
5. Da recomendaciones accionables para el próximo mes.
6. Responde en español, en formato JSON estructurado.

RESPUESTA ESPERADA (JSON):
{{
  "resumen_ejecutivo": "resumen de 2-3 líneas sobre el desempeño del período",
  "productos_estrella": [
    {{ "nombre": "producto", "ventas": número, "ingresos": número }}
  ],
  "productos_atencion": [
    {{ "nombre": "producto", "razón": "por qué necesita atención" }}
  ],
  "alertas_reabastecimiento": [
    {{ "producto": "nombre", "stock_actual": número, "stock_minimo": número, "urgencia": "baja|media|alta" }}
  ],
  "recomendaciones": [
    "recomendación 1",
    "recomendación 2"
  ],
  "tendencia_general": "positiva|negativa|estable",
  "proyeccion_siguiente_mes": "proyección breve"
}}

IMPORTANTE: Responde SOLAMENTE con el JSON, sin texto adicional antes o después."""

    return prompt
