import logging
import json
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger('django.request')

class AuthenticationLoggingMiddleware:
    """
    Middleware para registrar información detallada sobre solicitudes de autenticación
    para ayudar a depurar problemas.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # Solo registrar solicitudes relacionadas con autenticación
        if any(path in request.path for path in ['/token/', '/token/refresh/', '/auth/', '/employees/me/']):
            # Registrar detalles de la solicitud
            headers = {k: v for k, v in request.headers.items()}
            
            # Evitar registrar tokens completos por seguridad
            if 'Authorization' in headers:
                auth_header = headers['Authorization']
                if auth_header.startswith('Bearer ') and len(auth_header) > 15:
                    headers['Authorization'] = f"Bearer {auth_header[7:15]}..."
            
            # Registrar detalles importantes para depuración
            logger.info(f"Auth Request: {request.method} {request.path}")
            logger.info(f"Auth Headers: {json.dumps(headers, indent=2)}")
            
            # Para solicitudes POST intentamos registrar el cuerpo (excepto contraseñas)
            if request.method == 'POST' and hasattr(request, 'body'):
                try:
                    body = json.loads(request.body)
                    if isinstance(body, dict):
                        # Ocultar contraseñas y tokens por seguridad
                        if 'password' in body:
                            body['password'] = '*****'
                        if 'refresh' in body:
                            body['refresh'] = body['refresh'][:10] + '...'
                    logger.info(f"Auth Body: {json.dumps(body, indent=2)}")
                except:
                    # Si no podemos parsear como JSON, no registramos el cuerpo
                    pass
        
        # Continuar con la solicitud
        response = self.get_response(request)
        
        # Registrar detalles de la respuesta
        if any(path in request.path for path in ['/token/', '/token/refresh/', '/auth/', '/employees/me/']):
            logger.info(f"Auth Response: {response.status_code}")
            # Para errores, intentar registrar más detalles
            if response.status_code >= 400:
                try:
                    content = json.loads(response.content)
                    logger.warning(f"Auth Error: {json.dumps(content, indent=2)}")
                except:
                    pass
        
        return response
