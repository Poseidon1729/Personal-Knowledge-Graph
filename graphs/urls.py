from django.urls import path
from .views import create_map_view, map_detail_view, save_graph_positions
app_name = "graphs"

urlpatterns = [
    path("create_map_view/", create_map_view, name="create_map_view"),
    path("graphs/map/", map_detail_view, name="map_detail_view"),
    path("save_positions/", save_graph_positions, name="save_graph_positions"),
]