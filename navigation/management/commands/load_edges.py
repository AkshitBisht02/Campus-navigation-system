import json
from django.core.management.base import BaseCommand
from navigation.models import Node, Edge

class Command(BaseCommand):
    help = "Load edges from adjacency-list JSON"

    def handle(self, *args, **kwargs):
        with open("navigation/data/edges.json", "r") as f:
            data = json.load(f)

        for src_name, neighbors in data.items():
            src = Node.objects.get(name=src_name)

            for dst_name, weight in neighbors.items():
                dst = Node.objects.get(name=dst_name)

                Edge.objects.create(
                    source=src,
                    destination=dst,
                    weight=weight
                )

        self.stdout.write(self.style.SUCCESS("Edges loaded successfully"))
