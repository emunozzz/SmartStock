from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai_schema import PrediccionRequest, PrediccionResponse, ReporteRequest, ReporteResponse
from app.ai.prediccion_service import predecir_demanda
from app.ai.reporte_service import generar_reporte
from app.ai.graficas_service import (
    grafica_tendencia_ventas,
    grafica_ventas_mensuales,
    grafica_ventas_por_categoria,
    GRAFICAS_DIR,
)

router = APIRouter(prefix="/ai", tags=["Inteligencia Artificial"])


@router.post("/prediccion-demanda", response_model=PrediccionResponse)
def prediccion_demanda(
    request: PrediccionRequest,
    db: Session = Depends(get_db),
):
    try:
        resultado = predecir_demanda(db, request.dias_historial)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar predicción: {str(e)}",
        )

    return PrediccionResponse(**resultado)


@router.post("/reporte-ventas", response_model=ReporteResponse)
def reporte_ventas(
    request: ReporteRequest,
    db: Session = Depends(get_db),
):
    try:
        resultado = generar_reporte(db, request.dias)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar reporte: {str(e)}",
        )

    return ReporteResponse(**resultado)


@router.get("/grafica/tendencia")
def grafica_tendencia(
    dias: int = 30,
    db: Session = Depends(get_db),
):
    try:
        ruta = grafica_tendencia_ventas(db, dias)
        return FileResponse(ruta, media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar gráfica: {str(e)}",
        )


@router.get("/grafica/mensuales")
def grafica_mensuales(
    meses: int = 6,
    db: Session = Depends(get_db),
):
    try:
        ruta = grafica_ventas_mensuales(db, meses)
        return FileResponse(ruta, media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar gráfica: {str(e)}",
        )


@router.get("/grafica/categoria")
def grafica_categoria(
    dias: int = 30,
    db: Session = Depends(get_db),
):
    try:
        ruta = grafica_ventas_por_categoria(db, dias)
        return FileResponse(ruta, media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar gráfica: {str(e)}",
        )
