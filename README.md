# South Sounds Explorer 🎵

Explorador de música electrónica latinoamericana construido con **FastAPI** y **Vanilla JS**, potenciado por la API de **Discogs**.

## Requisitos
- **Python 3.12+**
- **uv** (Gestor de paquetes de Python)
- **Discogs Personal Access Token**

## Instalación

1. **Clonar/Abrir** el proyecto.
2. **Configurar Entorno**:
   - Crea un archivo `.env` en la raíz con tus credenciales de Discogs:
     ```env
     DISCOGS_CONSUMER_KEY="tu_key"
     DISCOGS_CONSUMER_SECRET="tu_secret" 
     # Nota: Actualmente usamos autenticación simple de Discogs, 
     # asegúrate de que tu cliente esté configurado correctamente.
     ```
3. **Instalar Dependencias**:
   ```bash
   uv sync
   ```

## Cómo Iniciar 🚀

Necesitas dos terminales abiertas:

### Terminal 1: Backend (API)
Inicia el servidor de FastAPI:
```bash
uv run scripts/start_backend.py
```
> El backend correrá en: `http://localhost:8000`
>
> Documentación interactiva (Swagger): `http://localhost:8000/docs`

### Terminal 2: Frontend (UI)
Inicia el servidor estático para la interfaz:
```bash
uv run scripts/start_frontend.py
```
> El frontend correrá en: `http://localhost:5500`

## Características y Uso

- **Búsqueda Filtrada**: Busca artistas y el sistema filtrará automáticamente releases de **Latinoamérica** y géneros **Electrónicos** (Techno, House, Dubstep, IDM, etc.).
- **Ordenamiento**: Usa el selector en la UI para ver los lanzamientos "Destacados" (Relevancia) o los "Más Recientes".

## Testing 🧪

Los tests se encuentran en `backend/tests`.

- **Tests Automáticos** (pytest):
  ```bash
  uv run python -m pytest
  ```

- **Verificación Manual** (Script):
  ```bash
  uv run backend/tests/verify_discogs_manual.py
  ```

## Estructura del Proyecto

- `/backend`: Lógica del servidor (FastAPI).
  - `/app/api`: Definición de rutas y endpoints.
  - `/app/core`: Configuraciones.
  - `/app/services`: Integración con **Discogs** (`discogs.py`).
  - `/tests`: Tests unitarios y manuales.
- `/frontend`: Interfaz de usuario (HTML/CSS/JS).
- `/scripts`: Scripts de ejecución (`start_backend.py`, `start_frontend.py`).
- `/logs`: Archivos de registro de la aplicación.
