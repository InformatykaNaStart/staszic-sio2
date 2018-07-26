from oioioi.base import admin
from models import PolygonImportRequest

class PolygonImportRequestAdmin(admin.ModelAdmin):
    list_display = ['problem_id', 'contest', 'problem_name', 'status']

admin.site.register(PolygonImportRequest, PolygonImportRequestAdmin)

