from django.apps import AppConfig

class GraphsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphs'

    def ready(self):
        import threading
        import time

        def keep_alive():
            while True:
                time.sleep(300)
                try:
                    from .neo4j_client import get_driver
                    get_driver().verify_connectivity()
                except Exception:
                    pass

        t = threading.Thread(target=keep_alive, daemon=True)
        t.start()