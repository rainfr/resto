from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICES = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Client')
    )

    first_name = models.CharField(max_length=30, default='give a first_name')
    last_name = models.CharField(max_length=30, default='give a last_name')
    username = models.CharField(max_length=30, unique=True, null=False, blank=False, default='give a username')
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False, default='give a email')
    phone_number = models.CharField(max_length=30, unique=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=False)

    # required fields
    date_joined = models.DateTimeField(auto_now=True, null=False, blank=False)
    last_login = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    modified_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    is_admin = models.BooleanField(default=False, null=False, blank=False)
    is_staff = models.BooleanField(default=False, null=False, blank=False)
    is_active = models.BooleanField(default=False, null=False, blank=False)
    is_superadmin = models.BooleanField(default=False, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
            return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    adress_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    modified = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.user.email
