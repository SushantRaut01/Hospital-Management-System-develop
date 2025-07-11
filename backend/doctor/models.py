from django.db import models
from assistant.models import Patient_Data
from django.utils.text import slugify
import uuid


class Medicine(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        # Normalize name and generate UUIDv5 based on name
        self.name = self.name.strip().title()
        if not self.uid:
            self.uid = uuid.uuid5(uuid.NAMESPACE_DNS, slugify(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Stores each prescription issued by doctor
class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient_Data,
        on_delete=models.CASCADE,
        to_field='pid',
        db_column='pid',
        related_name='prescriptions'
    )
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    medicine_name = models.CharField(max_length=255)
    dose = models.CharField(max_length=50)
    frequency = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    prescription_round = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.patient.pid} - Visit {self.prescription_round} - {self.medicine_name}"

