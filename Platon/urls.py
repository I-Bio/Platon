from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from main.views.errors.custom403View import Custom403View
from main.views.errors.custom404View import Custom404View
from main.views.errors.custom500View import Custom500View

handler403 = Custom403View.as_view()
handler404 = Custom404View.as_view()
handler500 = Custom500View.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



