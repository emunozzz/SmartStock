import json
from groq import Groq
from sqlalchemy.orm import Session

from app.core.config import settings
from app.ai.prompt_builder import construir_prompt_reporte
from app.ai.graficas_service import generar_todas_las_graficas, GRAFICAS_DIR


client = Groq(api_key=settings.GROQ_API_KEY)


def generar_reporte(db: Session, dias: int = 30) -> dict:
    prompt = construir_prompt_reporte(db, dias)

    respuesta = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Eres un analista financiero y de inventario experto. Respondes siempre en JSON válido, sin texto adicional.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    contenido = respuesta.choices[0].message.content.strip()

    if contenido.startswith("```"):
        lineas = contenido.split("\n")
        lineas = [l for l in lineas if not l.strip().startswith("```")]
        contenido = "\n".join(lineas)

    try:
        resultado = json.loads(contenido)
    except json.JSONDecodeError:
        resultado = {
            "resumen_ejecutivo": contenido,
            "productos_estrella": [],
            "productos_atencion": [],
            "alertas_reabastecimiento": [],
            "recomendaciones": [],
            "tendencia_general": "desconocida",
            "proyeccion_siguiente_mes": "No se pudo generar",
            "raw_response": contenido,
        }

    graficas_fs = generar_todas_las_graficas(db, dias)
    graficas = [g.replace(GRAFICAS_DIR, "/static/graficas").replace("\\", "/") for g in graficas_fs]

    resultado["graficas"] = graficas
    resultado["modelo_usado"] = settings.GROQ_MODEL
    resultado["tokens_utilizados"] = (
        respuesta.usage.total_tokens if respuesta.usage else 0
    )

    return resultado
