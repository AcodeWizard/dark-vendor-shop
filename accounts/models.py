from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q
from django.db.models.signals import pre_save, post_save


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, level='Member', is_staff=False, is_admin=False):

        user_obj = self.model(
            username=username,
        )
        user_obj.set_password(password)
        user_obj.level = level
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = True
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            level='Staff',
        )
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            is_admin=True,
            level='Admin'
        )
        return user


USER_LEVEL = (
    ('Administrator', 'Admin'),
    ('Staff', 'Staff'),
    ('Vendor', 'Vendor'),
    ('Member', 'Member'),
)


class User(AbstractBaseUser):
    username        = models.CharField(max_length=120, unique=True)
    pgp_key         = models.TextField(null=True, blank=True)
    image           = models.ImageField(upload_to='accounts/%Y/%m/%d', blank=True)
    level           = models.CharField(max_length=120, choices=USER_LEVEL, default='Member')
    admin           = models.BooleanField(default=False)    # superuser
    staff           = models.BooleanField(default=False)    # staff but not superuser
    vendor          = models.BooleanField(default=False)    # user is a seller
    is_active       = models.BooleanField(default=True)     # user can login
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    tfalogin        = models.BooleanField(default=False)    # 2fa pgp login enabled?

    USERNAME_FIELD = 'username'

    # USERNAME_FIELD and password are required by default.

    # Sets fields required at Sign-up
    # REQUIRED_FIELDS = ['']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_vendor(self):
        return self.admin

    @property
    def get_pgp_key(self):
        return self.pgp_key

    @property
    def is_tfa_login(self):
        return self.tfalogin



class VendorTerm(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Vendor ID",related_name='+',null=True)
    description = models.CharField(max_length=2000)