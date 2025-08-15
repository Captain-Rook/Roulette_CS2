from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, steam_id, **extra_fields):
        if not steam_id:
            raise ValueError("Steam ID is required")
        user = self.model(steam_id=steam_id, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user
