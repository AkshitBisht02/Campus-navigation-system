from django.db import models

# Model for Nodes
class Node(models.Model):

    NODE_TYPES = (
        ("Building", "Building"),
        ("Road", "Road"),
    )

    name=models.CharField(max_length=100,null=False,blank=False)
    longitude=models.DecimalField(max_digits=9, decimal_places=6)
    latitude=models.DecimalField(max_digits=9, decimal_places=6)
    type=models.CharField(max_length=10, choices=NODE_TYPES)


# Model for edge
class Edge(models.Model):
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="outgoing_edges"
    )
    destination = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="incoming_edges"
    )
    weight = models.FloatField()


 
