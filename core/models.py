from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            first_name,
            last_name,
            password,
            is_superuser=False,
            is_admin=False
    ):
        password_invalid = validate_password(password, user=User)
        if password_invalid:
            return password_invalid

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        return self.create_user(
            email,
            first_name,
            last_name,
            password,
            is_superuser=True,
            is_admin=True
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    @property
    def is_staff(self):
        return self.is_admin


class Asset(models.Model):
    name = models.CharField(max_length=55)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=55)  # "stock", "currency", "crypto"


class AssetPair(models.Model):
    base_asset = models.ForeignKey(
        Asset,
        related_name='base_asset',
        on_delete=models.PROTECT
    )
    quote_asset = models.ForeignKey(
        Asset,
        related_name='quote_asset',
        on_delete=models.PROTECT
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['base_asset', 'quote_asset'],
                name='AssetPair unique'
            )
        ]


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('executed', 'Executed'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    asset_pair = models.ForeignKey(AssetPair, on_delete=models.PROTECT)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class Quote(models.Model):
    asset_pair = models.OneToOneField(
        AssetPair,
        related_name='quote',
        on_delete=models.CASCADE
    )
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2)

    def update_quote(self):
        ...
