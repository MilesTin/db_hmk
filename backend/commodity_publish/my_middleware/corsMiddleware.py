from rest_framework.response import Response
class ExposeHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        headers = ["Content-Length"]
        result = ",".join(headers)
        if isinstance(response, Response):
            response['Access-Control-Expose-Headers'] = result
            response.data['sessionid'] = request.session.session_key
            response._is_rendered = False
            response.render()
        # response['cookie'] = dict(request.session.user)
        # Code to be executed for each request/response after
        # the view is called.
        return response