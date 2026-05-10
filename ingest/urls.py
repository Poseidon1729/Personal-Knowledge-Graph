from django.urls import path
from .views import post_document
from .views import DocDeleteView

urlpatterns=[
    path("post_document/", post_document,name="post_document"),
    path("post_document/<int:pk>/delete/", DocDeleteView.as_view(), name="post_delete"),
]
