from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        
        if not email:
            raise ValueError("Users must have a valid email address.")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email = email,
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, password=None):
        
        user = self.create_user(email, name, password = password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email      = models.EmailField(max_length=150, unique=True)
    name       = models.CharField(max_length=150)
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    role       = models.PositiveSmallIntegerField(
                    choices = (
                                (1, 'Admin'),
                                (2, 'Teacher'),
                                (3, 'Student')
                              ), blank=False, null=False
                 )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

