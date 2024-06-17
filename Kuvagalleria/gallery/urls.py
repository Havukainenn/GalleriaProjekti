from django.urls import path
from .views import home, personal_gallery, register, custom_logout, viewImage, uploadImage
from . import views
urlpatterns = [
    path('', home, name='home'),
    path('personal_gallery/', personal_gallery, name='personal_gallery'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='custom_logout'),
    path('image/<int:pk>/', views.viewImage, name='view_image'), 
    path('upload/', views.uploadImage, name='upload_image'),  
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
