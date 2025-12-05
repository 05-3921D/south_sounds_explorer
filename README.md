# South Sounds Explorer 🎵

Explorador de música sudamericana consruido con **FastAPI** y **Vanilla JS**.

## Requisitos
- **Python 3.12+**
- **uv** (Gestor de paquetes de Python)
- Credenciales de Spotify Developer

## Instalación

1. **Clonar/Abrir** el proyecto.
2. **Configurar Entorno**:
   - Crea un archivo `.env` en la raíz (usa `.env.example` como guía si existe, o crea uno con:
     ```
     SPOTIFY_CLIENT_ID="tu_id"
     SPOTIFY_CLIENT_SECRET="tu_secreto"
     ```
3. **Instalar Dependencias**:
   ```En la consola
   uv sync
   ```

## Cómo Iniciar 🚀

Necesitas dos terminales abiertas:

### Terminal 1: Backend (API)
Inicia el servidor de FastAPI:
```bash
uv run main.py
```
> El backend correrá en: `http://localhost:8000`

### Terminal 2: Frontend (UI)
Inicia el servidor estático para la interfaz:
```bash
uv run start_frontend.py
```
> El frontend correrá en: `http://localhost:5500`

## Endpoints Principales

- `GET /api/search?q={query}`: Busca álbumes y canciones.
- `GET /api/health`: Verifica si el backend está vivo.
- `GET /docs`: Documentación interactiva automática (Swagger UI).

## Estructura del Proyecto

- `/app`: Código fuente del Backend (FastAPI).
- `/frontend`: Código fuente de la UI (HTML/CSS/JS).
- `/tests`: Scripts de prueba.
