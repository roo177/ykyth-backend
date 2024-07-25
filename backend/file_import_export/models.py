from django.db import models
from users.models import User


# Create your models here.
class FileImportExportStatus(models.Model):
    #TODO: Change max field char of file_name to 255 to prevent errors
    file_name = models.CharField(max_length=255, blank=False, null=False)
    file_type = models.CharField(max_length=255)
    file_process_type = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.PROTECT)
    file_status = models.CharField(max_length=50)
    path = models.FilePathField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "File Import Export Status"
        db_table = "file_import_export_status"
        ordering = ['id']

    def __str__(self):
        return self.file_name + " " + self.file_status