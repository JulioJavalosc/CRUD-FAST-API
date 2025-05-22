from fastapi import Request
from fastapi.responses import RedirectResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

async def session_middleware(request: Request, call_next):
    logging.info(f"Solicitud recibida para ruta: {request.url.path}")

    # Rutas públicas (sin validación de sesión)
    public_routes = ["/", "/usuarios/validate/", "/logout/", "/favicon.ico", "/docs", "/login"]
    
    if request.url.path in public_routes:
        logging.info(f"Ruta pública detectada: {request.url.path}")
        response = await call_next(request)
        return response

    try:
        if not request.session.get("user_id"):
            logging.info("Sesión no válida, redirigiendo a /")
            return RedirectResponse(url="/")

        logging.info("Sesión válida, continuando con la solicitud.")
    except Exception as e:
        logging.error(f"Error inesperado en middleware: {e}")
        return RedirectResponse(url="/")

    response = await call_next(request)
    return response