from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from user_agents import parse
from account.models import LoginHistory

@receiver(user_logged_in)
def save_login_history(sender, request, user, **kwargs):
    user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

    LoginHistory.objects.create(
        user=user,
        browser=f"{user_agent.browser.family} {user_agent.browser.version_string}",
        device=f"{user_agent.device.family} ({user_agent.os.family} {user_agent.os.version_string})",
        date=now(),
        ipAddress=get_client_ip(request)
    )

def get_client_ip(request):
    """IP manzilni aniqlovchi yordamchi funksiya"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
