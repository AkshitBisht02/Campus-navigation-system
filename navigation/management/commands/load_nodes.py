import json
from django.core.management.base import BaseCommand
from navigation.models import Node

class Command(BaseCommand):
    help = "Load nodes from JSON file"

    def handle(self, *args, **kwargs):
        with open("navigation/data/nodes.json", "r") as f:
            data = json.load(f)

        for name, coord in data.items():
            node_type = "ROAD" if "Road Point" in name else "BUILDING"

            Node.objects.create(
                name=name,
                latitude=coord["lat"],
                longitude=coord["lng"],
                type=node_type
            )

        self.stdout.write(self.style.SUCCESS("Nodes loaded successfully"))
