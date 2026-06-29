from django.contrib import admin
from .models import Record, RecordType, RecordStatus, RecordCategory, RecordSubcategory

admin.site.register(Record)
admin.site.register(RecordType)
admin.site.register(RecordStatus)
admin.site.register(RecordCategory)
admin.site.register(RecordSubcategory)
