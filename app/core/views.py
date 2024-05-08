from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from waste.models import *
from .utils import is_sts_manager, is_system_admin, is_landfill_manager
from .utils import aws_map_route_api
from report.views import (
    admin_generate_waste_transfer_volume_data_last_7_days,
    admin_generate_waste_transfer_fuel_cost_data_last_7_days,
    sts_manager_generate_waste_transfer_volume_data_last_7_days,
    sts_manager_generate_waste_transfer_fuel_cost_data_last_7_days,
    landfill_manager_generate_waste_transfer_volume_data_last_7_days,
    landfill_manager_generate_waste_transfer_fuel_cost_data_last_7_days,
)


def dashboard(request):
    group = request.user.groups.first()
    context = TemplateLayout.init(request, {'group': group})

    if is_system_admin(request.user):
        sts_list = STS.objects.all()
        landfill_list = Landfill.objects.all()
        ongoing_waste_transfers = WasteTransfer.objects.exclude(
            status='Completed').order_by('-id').all()
        volume_data_last7_days_keys, volume_data_last7_days_values = admin_generate_waste_transfer_volume_data_last_7_days()

        fuel_cost_data_last7_days_keys, fuel_cost_data_last7_days_values = admin_generate_waste_transfer_fuel_cost_data_last_7_days()
        context.update({
            'sts_list': sts_list,
            'landfill_list': landfill_list,
            'ongoing_waste_transfers': ongoing_waste_transfers,
            'volume_data_last7_days_keys': volume_data_last7_days_keys,
            'volume_data_last7_days_values': volume_data_last7_days_values,
            'fuel_cost_data_last7_days_keys': fuel_cost_data_last7_days_keys,
            'fuel_cost_data_last7_days_values': fuel_cost_data_last7_days_values,
        })
        return render(request, 'system_admin/dashboard.html', context)

    elif is_sts_manager(request.user):
        sts = STSManager.objects.get(user=request.user).sts
        waste_transfers = WasteTransfer.objects.filter(sts=sts).exclude(
            status='Completed').order_by('-id').all()

        volume_data_last7_days_keys, volume_data_last7_days_values = sts_manager_generate_waste_transfer_volume_data_last_7_days(
            sts)

        fuel_cost_data_last7_days_keys, fuel_cost_data_last7_days_values = sts_manager_generate_waste_transfer_fuel_cost_data_last_7_days(
            sts)

        context.update({
            'sts': sts,
            'waste_transfers': waste_transfers,
            'volume_data_last7_days_keys': volume_data_last7_days_keys,
            'volume_data_last7_days_values': volume_data_last7_days_values,
            'fuel_cost_data_last7_days_keys': fuel_cost_data_last7_days_keys,
            'fuel_cost_data_last7_days_values': fuel_cost_data_last7_days_values,
        })
        return render(request, 'sts_manager/dashboard.html', context)

    elif is_landfill_manager(request.user):
        landfill = LandfillManager.objects.get(user=request.user).landfill
        waste_transfers = WasteTransfer.objects.filter(landfill=landfill).exclude(
            status='Completed').order_by('-id').all()

        volume_data_last7_days_keys, volume_data_last7_days_values = landfill_manager_generate_waste_transfer_volume_data_last_7_days(
            landfill)

        fuel_cost_data_last7_days_keys, fuel_cost_data_last7_days_values = landfill_manager_generate_waste_transfer_fuel_cost_data_last_7_days(
            landfill)

        context.update({
            'landfill': landfill,
            'waste_transfers': waste_transfers,
            'volume_data_last7_days_keys': volume_data_last7_days_keys,
            'volume_data_last7_days_values': volume_data_last7_days_values,
            'fuel_cost_data_last7_days_keys': fuel_cost_data_last7_days_keys,
            'fuel_cost_data_last7_days_values': fuel_cost_data_last7_days_values,
        })
        return render(request, 'landfill_manager/dashboard.html', context)

    return render(request, 'common/dashboard.html', context)


def under_maintenance(request):
    context = TemplateLayout.init(request, {})
    # Update the context
    context.update(
        {
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),

        }
    )
    return render(request, 'common/under_maintenance.html', context)
