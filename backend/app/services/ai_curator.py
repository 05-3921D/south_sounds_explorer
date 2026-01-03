import google.generativeai as genai
import json
import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class AICurator:
    def __init__(self):
        self.enabled = bool(settings.GEMINI_API_KEY)
        if self.enabled:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            logger.warning("Curaduría IA desactivada: No se encontró GEMINI_API_KEY.")

    async def filter_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filtra una lista de lanzamientos musicales usando un LLM para eliminar
        música mainstream/pop etiquetada incorrectamente como electrónica.
        """
        if not self.enabled or not items:
            return items

        # Preparamos el prompt
        # Enviamos una lista simplificada para ahorrar tokens y evitar confusiones
        
        candidates = []
        for idx, item in enumerate(items):
            title = item.get('title', 'Desconocido')
            styles = ", ".join(item.get('style', []))
            candidates.append(f"ID:{idx} | {title} | Estilos: {styles}")

        prompt = f"""
                ROL
        Eres un Curador Profesional de Música Electrónica Underground Latinoamericana, con experiencia real en cultura de club, sellos independientes y escenas locales. Tu criterio es estricto, conservador y anti-mainstream.

        OBJETIVO PRINCIPAL
        Filtrar una lista de lanzamientos y CONSERVAR ÚNICAMENTE música electrónica auténtica de club / underground, minimizando falsos positivos comerciales. La prioridad es la pureza de la escena, no la popularidad.

        PRINCIPIO FUNDAMENTAL
        Si existe duda razonable sobre el origen electrónico del artista → CONSERVA.
        Si existe certeza de que proviene del pop/rock mainstream → ELIMINA sin excepción.

        CRITERIOS DE ELIMINACIÓN ❌ (OBLIGATORIOS)

        1. Artistas Mainstream / Pop-Rock / POP / ROCK
        Elimina inmediatamente artistas cuya identidad principal NO sea electrónica, incluso si:
        - El release dice “House”, “Techno”, “Electronic”, “EDM”
        - Es un remix, rework o versión club

        Ejemplos (no exhaustivos):
        Madonna, Shakira, Lady Gaga, Britney Spears, Rihanna,
        Coldplay, U2, Muse, Radiohead,
        Black Eyed Peas, Pet Shop Boys, Depeche Mode (etapa comercial)

        2. Falsos Positivos Electrónicos
        Elimina:
        - Bandas de rock/pop haciendo “electrónica”
        - Proyectos electrónicos derivados del mainstream
        - Releases orientados a radio, charts o marketing comercial

        Señales de alerta:
        - Colaboraciones con cantantes pop
        - Estética mainstream evidente
        - Enfoque en branding por sobre cultura de club

        3. Electrónica Comercial / EDM
        Elimina:
        - EDM festivalero
        - Big Room / Mainstage
        - Tech House comercial orientado a charts o redes sociales

        4. Álbumes en Vivo de Artistas No Electrónicos
        Elimina álbumes en vivo de artistas pop/rock, aunque usen bases electrónicas.

        CRITERIOS DE CONSERVACIÓN ✅ (PRIORIDAD ALTA)

        1. Productores Electrónicos Legítimos
        Conserva productores de:
        Techno, House, Electro, Minimal, Dub Techno, Acid, Breaks, Ambient oscuro, Industrial, Experimental
        con enfoque real de club o underground.

        2. Artistas Desconocidos o Nuevos
        Si el artista no es claramente mainstream → CONSERVAR.
        Prioriza proyectos emergentes y escenas locales.

        3. Sellos Discográficos Electrónicos
        Conserva releases publicados por:
        - Sellos independientes
        - Netlabels
        - Colectivos electrónicos
        especialmente de Latinoamérica.

        CONTEXTO LATINOAMERICANO (IMPORTANTE)
        Valora positivamente:
        - Escenas locales (Chile, Argentina, Perú, Colombia, México, Brasil, etc.)
        - Sonidos híbridos pero club-centric
        - Electrónica experimental, tribal, dub, minimal, industrial

        INSTRUCCIONES FINALES
        No seas indulgente con el mainstream.
        No elimines por desconocimiento.
        Prefiere falsos negativos antes que falsos positivos comerciales.
        La misión es FILETE, no volumen.

        LISTA DE ENTRADA:
        {chr(10).join(candidates)}

        INSTRUCCIONES:
        Analiza cada ítem. Si detectas un artista mainstream, bórralo.
        Devuelve un JSON con "kept_ids" (lista de enteros).
        Ejemplo: {{"kept_ids": [1, 3, 4]}}
        """

        try:
            # Usamos llamada asíncrona si está disponible, o la estándar envuelta si no.
            # Google SDK soporta async nativo.
            response = await self.model.generate_content_async(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            result_text = response.text
            data = json.loads(result_text)
            kept_indices = set(data.get("kept_ids", []))
            
            # Reconstruimos la lista preservando el orden original
            filtered_items = [items[i] for i in kept_indices if 0 <= i < len(items)]
            
            logger.info(f"Curaduría IA: Entrada {len(items)} -> Conservados {len(filtered_items)}")
            return filtered_items

        except Exception as e:
            logger.error(f"Fallo en Curaduría IA: {e}")
            return items # A prueba de fallos: devolver lista original
