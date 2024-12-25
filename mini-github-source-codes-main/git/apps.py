from django.apps import AppConfig


class GitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'git'

    def ready(self):
        import os
        # from . import jobs

        # RUN_MAIN check to avoid running the code twice since manage.py runserver runs 'ready' twice on startup
        if os.environ.get('RUN_MAIN', None) != 'true':
            # jobs.start()
            pass

        