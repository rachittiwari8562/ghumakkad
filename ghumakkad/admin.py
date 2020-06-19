from django.contrib import admin
from .models import Place,District,Comments,Blog,Sd
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(Comments)
admin.site.register(Blog)
from import_export import resources
class SdResource(resources.ModelResource):
    class Meta:
        model = Sd
class SdAdmin(ImportExportModelAdmin):
    resource_class= SdResource

class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place
class PlaceAdmin(ImportExportModelAdmin):
    resource_class= PlaceResource

class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
class DistrictAdmin(ImportExportModelAdmin):
    resource_class= DistrictResource

admin.site.register(District,DistrictAdmin)
admin.site.register(Place,PlaceAdmin)
admin.site.register(Sd,SdAdmin)
