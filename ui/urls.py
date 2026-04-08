from django.urls import path
from .views import home, create_folder, folder_list, folder_detail,create_file, map_detail_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home, name='home'),
    path("create_folder/", create_folder, name="create_folder"),
    path("folder_detail/<int:folder_id>/", folder_detail, name="folder_detail"),
    path("", folder_list, name="folder_tree"),
    path("create_file/",create_file,name="create_file"),
    path("map/", map_detail_view, name="map_detail_view")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)