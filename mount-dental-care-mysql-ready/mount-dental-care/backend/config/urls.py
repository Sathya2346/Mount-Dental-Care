from pathlib import Path

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.http import FileResponse, Http404
from django.views.static import serve


def serve_media_with_cors(
    request,
    path,
    document_root=None,
    show_indexes=False,
):
    response = serve(
        request,
        path,
        document_root=document_root,
        show_indexes=show_indexes,
    )

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"

    return response


def index_response(index_file):
    # index.html points at hashed asset filenames (index-<hash>.js), so it must
    # never be cached by the browser: a stale copy keeps loading the previous
    # bundle after a rebuild, which looks like frontend changes "not applying".
    response = FileResponse(
        open(index_file, "rb"),
        content_type="text/html; charset=utf-8",
    )
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def serve_react(request, path=""):
    frontend_dist = Path(settings.FRONTEND_DIST).resolve()
    requested_path = (path or "").strip("/")

    if not requested_path:
        index_file = frontend_dist / "index.html"

        if index_file.exists():
            return index_response(index_file)

        raise Http404("React build not found")

    requested_file = (frontend_dist / requested_path).resolve()

    try:
        requested_file.relative_to(frontend_dist)
    except ValueError:
        raise Http404("Invalid path")

    if requested_file.is_file():
        return FileResponse(open(requested_file, "rb"))

    index_file = frontend_dist / "index.html"

    if index_file.exists():
        return index_response(index_file)

    raise Http404("React build not found")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("clinic.urls")),

    # STATIC FILES
    re_path(
        r"^static/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.STATIC_ROOT,
        },
    ),

    # MEDIA FILES
    re_path(
        r"^media/(?P<path>.*)$",
        serve_media_with_cors,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),

    # REACT — MUST BE LAST
    re_path(
        r"^(?P<path>.*)$",
        serve_react,
        name="react_frontend",
    ),
]