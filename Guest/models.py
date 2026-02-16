from django.db import models
from Admin.models import*
from django.utils import timezone

# Create your models here.

class tbl_user(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    user_gender=models.CharField(max_length=30)
    user_dob=models.DateField()
    user_photo=models.FileField(upload_to="Assets/User/Photo/")
    user_password=models.CharField(max_length=30)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)


class SIEMRule(models.Model):
    """
    Rule Configuration Interface (DB-driven)
    Example: 5 failed logins in 60 seconds
    """
    RULE_TYPES = (
        ("FAILED_LOGIN_BURST", "Failed Login Burst"),
    )

    name = models.CharField(max_length=120, unique=True)
    rule_type = models.CharField(max_length=40, choices=RULE_TYPES)
    enabled = models.BooleanField(default=True)

    threshold = models.PositiveIntegerField(default=5)     # e.g., 5
    window_seconds = models.PositiveIntegerField(default=60)  # e.g., 60 sec

    severity_default = models.IntegerField(default=7)  # 1-10
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({'ON' if self.enabled else 'OFF'})"


class SecurityEvent(models.Model):
    """
    Historical Event Store (normalized event schema)
    """
    EVENT_TYPES = (
        ("LOGIN_ATTEMPT", "Login Attempt"),
        ("LOGIN_SUCCESS", "Login Success"),
        ("LOGIN_FAILURE", "Login Failure"),
    )

    event_type = models.CharField(max_length=40, choices=EVENT_TYPES)
    ts = models.DateTimeField(default=timezone.now)

    actor = models.CharField(max_length=255, blank=True, default="")  # email/username
    src_ip = models.CharField(max_length=64, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")

    outcome = models.CharField(max_length=20, blank=True, default="")  # SUCCESS/FAILURE
    severity = models.IntegerField(default=1)

    # extra structured data
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["ts"]),
            models.Index(fields=["event_type", "ts"]),
            models.Index(fields=["actor", "ts"]),
            models.Index(fields=["src_ip", "ts"]),
        ]

    def __str__(self):
        return f"{self.ts} {self.event_type} {self.actor} {self.outcome}"


class SecurityAlert(models.Model):
    """
    Incident & Alert Manager (alert lifecycle)
    """
    STATUS = (
        ("OPEN", "Open"),
        ("ACK", "Acknowledged"),
        ("CLOSED", "Closed"),
    )

    created_at = models.DateTimeField(default=timezone.now)
    rule = models.ForeignKey(SIEMRule, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")

    severity = models.IntegerField(default=5)  # 1-10
    status = models.CharField(max_length=10, choices=STATUS, default="OPEN")

    actor = models.CharField(max_length=255, blank=True, default="")
    src_ip = models.CharField(max_length=64, blank=True, default="")

    # optional: link to a "representative" event
    event = models.ForeignKey(SecurityEvent, on_delete=models.SET_NULL, null=True, blank=True)

    acknowledged_at = models.DateTimeField(null=True, blank=True)
    ack_note = models.TextField(blank=True, default="")

    def __str__(self):
        return f"[{self.status}] Sev{self.severity} {self.title}"