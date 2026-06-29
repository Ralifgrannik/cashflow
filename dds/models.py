from django.db import models
from django.utils import timezone

class RecordType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RecordStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RecordCategory(models.Model):
    type = models.ForeignKey(RecordType, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('type', 'name')

    def __str__(self):
        return self.name

class RecordSubcategory(models.Model):
    category = models.ForeignKey(RecordCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return self.name

class Record(models.Model):
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(RecordStatus, on_delete=models.PROTECT)
    type = models.ForeignKey(RecordType, on_delete=models.PROTECT)
    category = models.ForeignKey(RecordCategory, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(RecordSubcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} {self.type} {self.amount}"
