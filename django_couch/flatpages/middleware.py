from annoying.decorators import render_to
from django.http import Http404
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

class FlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            return flatpage(request)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response

def flatpage(request):
    
    rows = request.db.view(settings.COUCHDB_FLATPAGES, key = request.path, include_docs = True).rows
    if rows:
        row = rows[0]


        return render_to_response('static.html', {'doc': row.doc}, RequestContext(request))
    else:
        raise Http404('Page not found')
    
