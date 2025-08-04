from django.http import HttpResponsePermanentRedirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        if host.startswith("www."):
            non_www_host = host[len("www."):]
            url = request.build_absolute_uri().replace(host, non_www_host, 1)
            return HttpResponsePermanentRedirect(url)

        return self.get_response(request)
