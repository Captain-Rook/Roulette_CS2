from django.core.management.base import BaseCommand
from oauth2_provider.models import Application


class Command(BaseCommand):
    def handle(self, *args, **options):
        app = Application.objects.create(
            name="cases",
            client_type="confidential",
            authorization_grant_type="password",
        )
        print(f"Client ID: {app.client_id}")
        print(f"Client Secret: {app.client_secret}")
