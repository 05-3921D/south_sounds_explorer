# South Sounds Explorer 🎵🌎

Explorador de música electrónica latinoamericana. Descubre gemas ocultas, desde Techno en Chile hasta House en Colombia, todo potenciado por la inmensa base de datos de **Discogs**.

🔗 **Live Demo**: [southsoundexplorer.netlify.app](https://southsoundexplorer.netlify.app)  
*(Backend hospedado en Render, puede tardar 30s en "despertar" la primera vez)*

## ✨ Características

*   **Búsqueda Inteligente**: Encuentra artistas y lanzamientos filtrados automáticamente por:
    *   🌍 Región: Solo países de Latinoamérica.
    *   🎹 Estilo: Solo géneros electrónicos (Techno, House, Ambient, etc.).
*   **Sugerencias Dinámicas**:
    *   **Por Género**: Descubre estilos aleatorios ("Tribal", "Dub Techno", "Deep House") cada vez que entras.
    *   **Por País**: Explora escenas locales aleatorias ("Peru", "Argentina", "Mexico").
*   **Ordenamiento**: Alterna fácilmente entre los resultados más **Relevantes** o los más **Recientes**.
*   **Paginación**: Carga infinita de resultados con el botón "Cargar más".
*   **Diseño Moderno**: Interfaz estilo "Glassmorphism" con scroll suave y chips interactivos.

## 🛠️ Tecnologías

### Backend
*   **Python 3.12**
*   **FastAPI**: API REST rápida y moderna.
*   **Httpx**: Cliente HTTP asíncrono para conectar con Discogs.
*   **Pydantic**: Validación de datos robusta.

### Frontend
*   **Vanilla JS**: Sin frameworks pesados, solo JS moderno y rápido.
*   **CSS3**: Variables CSS, Flexbox, Grid y efectos de transparencia.
*   **HTML5**: Semántico y accesible.

## 🚀 Instalación Local

1.  **Clonar** el proyecto.
2.  **Configurar Entorno**:
    Crea un archivo `.env` en la raíz con tus credenciales de [Discogs Developer](https://www.discogs.com/settings/developers):
    ```env
    DISCOGS_CONSUMER_KEY="tu_key"
    DISCOGS_CONSUMER_SECRET="tu_secret" 
    ```
3.  **Instalar Dependencias**:
    Requiere [uv](https://github.com/astral-sh/uv).
    ```bash
    uv sync
    ```

## ▶️ Cómo Ejecutar

Necesitas dos terminales abiertas:

**1. Backend (API)**
```bash
uv run scripts/start_backend.py
```
> Corre en: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

**2. Frontend (UI)**
```bash
uv run scripts/start_frontend.py
```
> Corre en: `http://localhost:5500`

## ☁️ Despliegue

El proyecto está configurado para un despliegue gratuito y escalable:
*   **Backend**: Render (Web Service).
*   **Frontend**: Netlify / Vercel (Static Site).

Consulta la guía detallada en [DEPLOY.md](./DEPLOY.md).

## 🧪 Testing

```bash
# Ejecutar tests automatizados
uv run python -m pytest
```

---

FTPWW 24-7 
🔥🔥👮‍♂️🚓🔥🔥
