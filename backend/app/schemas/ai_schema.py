from pydantic import BaseModel, Field


class PrediccionRequest(BaseModel):
    dias_historial: int = Field(
        default=90,
        ge=30,
        le=365,
        description="Días de historial de ventas a analizar (30-365)",
    )


class ProductoMayorTendencia(BaseModel):
    nombre: str = "Sin datos"
    variacion_pct: float = 0.0


class ProductoRiesgoQuiebre(BaseModel):
    nombre: str = "Sin datos"
    dias_restantes_stock: int = 0


class Insights(BaseModel):
    producto_mayor_tendencia: ProductoMayorTendencia = ProductoMayorTendencia()
    producto_riesgo_quiebre: ProductoRiesgoQuiebre = ProductoRiesgoQuiebre()
    precision_modelo_pct: float = 0.0


class ProyeccionPeriodo(BaseModel):
    periodo: str = ""
    demanda_historica: int | None = None
    demanda_proyectada: int = 0


class PrediccionResponse(BaseModel):
    insights: Insights = Insights()
    proyeccion: list[ProyeccionPeriodo] = []


class ReporteRequest(BaseModel):
    dias: int = Field(
        default=30,
        ge=7,
        le=365,
        description="Días del período a reportar (7-365)",
    )


class ProductoEstrella(BaseModel):
    nombre: str = "Desconocido"
    ventas: int = 0
    ingresos: float = 0.0


class ProductoAtencion(BaseModel):
    nombre: str = "Desconocido"
    razon: str = "Sin especificar"


class AlertaReabastecimiento(BaseModel):
    producto: str = "Desconocido"
    stock_actual: int = 0
    stock_minimo: int = 0
    urgencia: str = "baja"


class ReporteResponse(BaseModel):
    resumen_ejecutivo: str = ""
    productos_estrella: list[ProductoEstrella] = []
    productos_atencion: list[ProductoAtencion] = []
    alertas_reabastecimiento: list[AlertaReabastecimiento] = []
    recomendaciones: list[str] = []
    tendencia_general: str = "estable"
    proyeccion_siguiente_mes: str = ""
    graficas: list[str] = []
    modelo_usado: str = ""
    tokens_utilizados: int = 0
