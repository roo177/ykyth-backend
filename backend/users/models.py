import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # Kullanıcı ID'si
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Kullanıcının adı soyadı
    fullname = models.CharField(max_length=150, blank=True, null=True, verbose_name="Full Name")
    # Kullanıcı adı
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name="User Name")
    # Kullanıcı email adresi
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="E-Mail Address")
    # Kullanıcının Durumu
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    
    # Common modelden alamadığımız alanlar
    # AbstractUser kullandığımız için ayrıca Common modeli kullanamadık
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='created_by_field')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='updated_by_field')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='deleted_by_field')
    is_deleted = models.BooleanField(default=False)

    # Istenmeyen alanlar
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        if self.email:
            return self.email
        else:
            return super().__str__()

    class Meta: 
        verbose_name = 'Users'
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ['-created_at']
