from django.apps import AppConfig
import neomodel

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_residents_app'

    def ready(self):
        # Set the Neo4j Aura connection URL
        neomodel.config.DATABASE_URL = 'neo4j+s://neo4j:d3zda0Dd1DzVr_m7GfsPik_YFGlM-qfmdeCjZrxkKFc@d5e585c5.databases.neo4j.io'

        # Import the Neomodel app to ensure that neomodel is properly initialized
        import city_residents_app.models