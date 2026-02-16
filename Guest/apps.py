from django.apps import AppConfig


class GuestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Guest"

    def ready(self):
        # Auto-create default SIEM rule (safe)
        from django.db.utils import OperationalError
        from .models import SIEMRule

        try:
            SIEMRule.objects.get_or_create(
                name="Failed logins: 5 in 60s",
                defaults={
                    "rule_type": "FAILED_LOGIN_BURST",
                    "enabled": True,
                    "threshold": 5,
                    "window_seconds": 60,
                    "severity_default": 8,
                },
            )
        except OperationalError:
            # DB tables not ready during migrate
            pass
