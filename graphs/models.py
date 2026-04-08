from django.db import models

class GraphPosition(models.Model):
    graph_name = models.CharField(max_length=255)
    node_id = models.CharField(max_length=255)  # Node name/label
    x = models.FloatField()
    y = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['graph_name', 'node_id']

    def __str__(self):
        return f"{self.graph_name} - {self.node_id}: ({self.x}, {self.y})"
