"""compas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import nested_admin

@csrf_exempt
def ckeditor_upload(request):
    """
    Обработчик POST-запросов для загрузки изображений из CKEditor.
    Возвращает JSON с URL загруженного файла.
    """

    if request.method != 'POST':
        return JsonResponse({'uploaded': False, 'error': {'message': 'Method not allowed'}}, status=405)

    try:
        if 'upload' not in request.FILES:
            return JsonResponse({'uploaded': False, 'error': {'message': 'No file provided'}}, status=400)

        upload_file = request.FILES['upload'] #получаем файл

        # валидация расширений
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_ext = os.path.splitext(upload_file.name)[1].lower() #получаем расширение
        if file_ext not in allowed_extensions:
            return JsonResponse({'uploaded': False, 'error': {'message': 'Only images allowed'}}, status=400)

        # генерация уникального имени, защита от перезаписи
        import uuid
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"

        # путь для сохранения media/имя_файла
        file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

        with open(file_path, 'wb+') as destination: # w - write; b - binary
            for chunk in upload_file.chunks(): # разбиваем файл на чанки (для больших файлов)
                destination.write(chunk) # запись текущего куска в открытый файл destination

        # формируем url для доступа картинки из браузера
        url = f"{settings.MEDIA_URL}{unique_filename}"

        return JsonResponse({
            'uploaded': True,
            'url': url,
            'fileName': unique_filename,
        })

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.exception(f'Upload error: {str(e)}')
        return JsonResponse({'uploaded': False, 'error': {'message': str(e)}}, status=500)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("main/", TemplateView.as_view(template_name="main.html")),
    path('', include('catalog.urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/upload/', ckeditor_upload, name='ckeditor_upload'),
    path('nested-admin/', include('nested_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

