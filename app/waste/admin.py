from django.contrib import admin
from .models import *


admin.site.register(Path)


class WasteTransferAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WasteTransfer._meta.fields]
    list_per_page = 20


admin.site.register(WasteTransfer, WasteTransferAdmin)


class WasteTransferQueueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WasteTransferQueue._meta.fields]
    list_per_page = 20


admin.site.register(WasteTransferQueue, WasteTransferQueueAdmin)


class LandfillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Landfill._meta.fields]
    list_per_page = 20


admin.site.register(Landfill, LandfillAdmin)


class LandfillManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LandfillManager._meta.fields]
    search_fields = ('user', 'landfill')
    list_per_page = 20


admin.site.register(LandfillManager, LandfillManagerAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vehicle._meta.fields]
    search_fields = ('vehicle_number', 'type', 'capacity')
    list_per_page = 20


admin.site.register(Vehicle, VehicleAdmin)


class STSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in STS._meta.fields]
    search_fields = ('address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)


class STSManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in STSManager._meta.fields]
    search_fields = ('user', 'sts')
    list_per_page = 20


admin.site.register(STSManager, STSManagerAdmin)


# class ContractorAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Contractor._meta.fields]
#     list_per_page = 20


# admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Contractor)


class Contract_ContractorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contract_Contractor._meta.fields]
    list_per_page = 20


admin.site.register(Contract_Contractor, Contract_ContractorAdmin)


class ContractorManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContractorManager._meta.fields]
    list_per_page = 20


admin.site.register(ContractorManager, ContractorManagerAdmin)


class WorkforceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Workforce._meta.fields]
    list_per_page = 20


admin.site.register(Workforce, WorkforceAdmin)


class Workforce_WorkHoursAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Workforce_WorkHours._meta.fields]
    list_per_page = 20


admin.site.register(Workforce_WorkHours, Workforce_WorkHoursAdmin)


class WasteTransferToStsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WasteTransferToSts._meta.fields]
    list_per_page = 20


admin.site.register(WasteTransferToSts, WasteTransferToStsAdmin)


class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Neighborhood._meta.fields]
    list_per_page = 20


admin.site.register(Neighborhood, NeighborhoodAdmin)
