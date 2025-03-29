import secrets
from fastapi import Request
import logging
def create_random_session_string() -> str:
    return secrets.token_urlsafe(32)
from datetime import datetime, timedelta

def validate_session(request: Request) -> bool:
    # Obtener datos de la cookie y la sesión
    user_id = request.session.get("user_id")
    session_authorization = request.cookies.get("Authorization")
    session_id = request.session.get("session_id")
    session_access_token = request.session.get("access_token")
    token_exp = request.session.get("token_expiry")

    # Verificar que existan los datos necesarios
    if not session_authorization or not session_id or not session_access_token or not token_exp or not user_id:
        logging.info("Missing session data, redirecting to login")
        return False

    # Verificar que el Authorization coincida con el session_id
    if session_authorization != session_id:
        logging.info("Authorization does not match Session Id, redirecting to login")
        return False

    # Verificar si el token ha expirado
    if is_token_expired(token_exp):
        logging.info("Access_token is expired, redirecting to login")
        return False

    logging.info("Valid Session, Access granted.")
    return True


def is_token_expired(unix_timestamp: int) -> bool:
    if unix_timestamp:
        datetime_from_unix = datetime.fromtimestamp(unix_timestamp)
        current_time = datetime.now()
        difference_in_minutes = (datetime_from_unix - current_time).total_seconds() / 60
        return difference_in_minutes <= 0
    
    return True