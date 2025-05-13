import uuid

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = str(uuid.uuid4())  # Crée un ID unique
        response = self.get_response(request)
        response["X-Request-ID"] = request.id
        return response