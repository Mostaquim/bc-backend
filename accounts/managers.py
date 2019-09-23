from django.contrib.auth.models import UserManager as UM

class UserManager(UM):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


    def create_user_phone(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        email = phone_number + '@bashachai.com'
        extra_fields.setdefault('email',email)
        
        return self._create_user( phone_number, password, **extra_fields )