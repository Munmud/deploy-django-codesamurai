from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import re_path

from authentication import views as auth_app
from waste import views as waste_app
from web_project.views import SystemView
from core.views import dashboard, under_maintenance
from notification.consumers import NotificationConsumer
from notification import views as notification_app


urlpatterns = [
    #     path("notification", notification_app.notification_page_view,
    #          name="notification_page"),
    path('admin/', admin.site.urls, name='admin_dashboard'),
    path('captcha/', include('captcha.urls')),
    path('under_maintenance', under_maintenance, name='under_maintenance'),

    # workforce add_workforce_work_hours
    path('add_workforce_work_hours/', waste_app.add_workforce_work_hours,
         name="add_workforce_work_hours"),

    # contract_manager
    path('workforce_registration/', waste_app.workforce_registration,
         name="workforce_registration"),
    path('workforce_work_hours/', waste_app.workforce_work_hours,
         name="workforce_work_hours"),


    # notification
    path('view_all_notification', notification_app.read_all_notification,
         name="read_all_notification"),

    # auth
    path('auth/login', auth_app.user_login, name='login'),
    path('auth/logout', auth_app.user_logout, name='logout'),
    #     path('auth/create', auth_app.register, name='register'),
    path('auth/forget-password/', auth_app.ForgetPassword, name="forget_password"),
    path('auth/change-password/<token>/',
         auth_app.ChangePassword, name="change_password"),
    path('auth/change-user-password/',
         auth_app.ChangePasswordByUser, name="change_user_password"),
    path('auth/update-profile/',
         auth_app.update_profile, name="update_profile"),

    # Ststem Admin
    #     path('system_admin/add_vehicle/', waste_app.add_vehicle, name="add_vehicle"),

    # STS Manager  get_schedule_sugggestion

    path('sts_manager/get_schedule_sugggestion',
         waste_app.get_schedule_sugggestion, name="get_schedule_sugggestion"),

    path('sts_manager/contractor_bill',
         waste_app.get_contractor_bill, name="get_contractor_bill"),

    path('sts_manager/waste_transfer/<int:pk>',
         waste_app.add_waste, name="add_waste"),

    path('sts_manager/transfer_waste/start',
         waste_app.waste_transfer_start, name="waste_transfer_start"),

    path('sts_manager/sts_add_new_waste',
         waste_app.sts_add_new_waste, name="sts_add_new_waste"),


    path('sts_manager/transfer_waste/start_complete',
         waste_app.waste_transfer_start_complete, name="waste_transfer_start_complete"),

    path('sts_manager/transfer_waste/complete/<int:transfer_id>',
         waste_app.waste_transfer_complete, name="waste_transfer_complete"),

    path('sts_manager/transfer_waste/create_fleet_step_1',
         waste_app.create_fleet_step_1, name="create_fleet_step_1"),

    path('sts_manager/transfer_waste/create_fleet_step_2',
         waste_app.create_fleet_step_2, name="create_fleet_step_2"),


    # landfill manager
    path('landfill_manager/transfer_waste/dump_start/<int:transfer_id>',
         waste_app.waste_transfer_start_dumping, name="waste_transfer_start_dumping"),
    path('landfill_manager/transfer_waste/dump_end/<int:transfer_id>',
         waste_app.waste_transfer_end_dumping, name="waste_transfer_end_dumping"),
    path('landfill_manager/transfer_waste/report/<int:transfer_id>',
         waste_app.waste_transfer_generate_bill, name="waste_transfer_generate_bill"),

    #     path('sts_manager/transfer_waste/edit/<int:transfer_id>',
    #          waste_app.edit_waste_transfer, name="edit_waste_transfer"),

    # common waste_transfer_details
    path('waste_transfer/<int:transfer_id>',
         waste_app.waste_transfer_details, name="waste_transfer_details"),


    path('', dashboard, name='dashboard'),

]

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi())
]


# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = SystemView.as_view(
    template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(
    template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(
    template_name="pages_misc_error.html", status=500)
