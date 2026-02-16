from datetime import timedelta
from django.utils import timezone

from .models import SecurityEvent, SecurityAlert, SIEMRule


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def log_event(*, event_type, request, actor="", outcome="", severity=1, details=None):
    if details is None:
        details = {}

    ev = SecurityEvent.objects.create(
        event_type=event_type,
        actor=actor or "",
        src_ip=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") or "",
        outcome=outcome or "",
        severity=int(severity),
        details=details,
    )

    try_run_correlation(ev)
    return ev


def try_run_correlation(ev: SecurityEvent):
    # Only for failed login burst rule
    if ev.event_type != "LOGIN_FAILURE":
        return

    rules = SIEMRule.objects.filter(enabled=True, rule_type="FAILED_LOGIN_BURST")

    for rule in rules:
        window_start = timezone.now() - timedelta(seconds=rule.window_seconds)

        qs = SecurityEvent.objects.filter(event_type="LOGIN_FAILURE", ts__gte=window_start)

        if ev.actor:
            qs = qs.filter(actor=ev.actor)
        if ev.src_ip:
            qs = qs.filter(src_ip=ev.src_ip)

        fail_count = qs.count()

        if fail_count >= rule.threshold:
            # avoid spam alerts in same window
            exists = SecurityAlert.objects.filter(
                rule=rule,
                status="OPEN",
                actor=ev.actor,
                src_ip=ev.src_ip,
                created_at__gte=window_start,
            ).exists()

            if not exists:
                SecurityAlert.objects.create(
                    rule=rule,
                    title=f"Possible brute force: {fail_count} failed logins in {rule.window_seconds}s",
                    description=(
                        f"Detected {fail_count} failed login attempts within {rule.window_seconds} seconds "
                        f"for actor='{ev.actor}' from ip='{ev.src_ip}'."
                    ),
                    severity=rule.severity_default,
                    actor=ev.actor,
                    src_ip=ev.src_ip,
                    event=ev,
                )
