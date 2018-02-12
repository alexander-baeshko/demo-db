from django.db import models
from django_mysql.models import JSONField
import uuid

# Create your models here.
class Dmdb(models.Model):
    id_obj = models.AutoField(primary_key=True)
    tx_obj = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    timestamp_obj = models.DateTimeField(auto_now_add=True)
    json_obj = JSONField()
