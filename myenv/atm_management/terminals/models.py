# terminals/models.py
from django.db import models

class Terminal(models.Model):
   
    unit_id = models.CharField(max_length=10)
    terminal_id = models.CharField(max_length=50)
    terminal_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    port = models.CharField(max_length=10)
    ip = models.GenericIPAddressField()
    location = models.CharField(max_length=10)
    type = models.CharField(max_length=20, default="Hitachi CRM")
    status = models.CharField(max_length=50, default='Operational')  # New field

    def __str__(self):
        return self.terminal_name
