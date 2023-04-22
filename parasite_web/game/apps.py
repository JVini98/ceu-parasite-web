from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    # Import the signal once the application is loaded and ready to run
    def ready(self):
        import game.signals