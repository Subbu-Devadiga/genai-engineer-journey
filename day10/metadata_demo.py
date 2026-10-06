documents=[
     {
        "id": "normal_change",
        "text": "Normal changes follow the standard change management process.",
        "metadata": {
            "category": "change",
            "type": "normal",
            "environment": "all"
        }
    },
    {
        "id": "emergency_change",
        "text": "Emergency changes address critical incidents, outages, security issues, or other urgent situations.",
        "metadata": {
            "category": "change",
            "type": "emergency",
            "environment": "production"
        }
    },
    {
        "id": "production_validation",
        "text": "Production changes should include application health checks, functional testing, monitoring, and log verification.",
        "metadata": {
            "category": "change",
            "type": "validation",
            "environment": "production"
        }
    },
    {
        "id": "incident_management",
        "text": "Incidents are assigned priority levels based on urgency and business impact.",
        "metadata": {
            "category": "incident",
            "type": "incident",
            "environment": "production"
        }
    }
]

print("All Documents:")

for document in documents:
    print(document["id"],"-->",document["metadata"])

print("\nProduction Documents:")
for document in documents:
    if document["metadata"]["environment"]=="production":
        print(document["id"])
        