from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, name, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Provide a valid email')
        email = self.normalize_email(email)
        user = self.model(name=name, username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        return self._create_user(name, username, email, password, **extra_fields)

    def create_superuser(self, name, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(name, username, email, password, **extra_fields)