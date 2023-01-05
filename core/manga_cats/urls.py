from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home_app.urls")),
    path("auth/", include("user_app.urls")),
    path("manga/", include("manga_app.urls")),
    path("chapter/", include("chapter_app.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT  )