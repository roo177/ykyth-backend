import uuid
from django.db import models
from users.models import User

from django.db import models
import uuid
from django.conf import settings
def get_related_name(instance, field):
    return f"{instance.__class__.__name__.lower()}_{field}_set"


class Common(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_created_set', on_delete=models.PROTECT, blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_updated_set', on_delete=models.PROTECT, blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_deleted_set', on_delete=models.PROTECT, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True
