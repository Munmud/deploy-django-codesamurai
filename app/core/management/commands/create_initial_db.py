
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date

from core.utils import (
    create_system_admin,
    load_sts,
    load_vehicle
)
from waste.models import *

USER_STS = 'sts'
USER_Landfill = 'landfill'
USER_Contractor = 'contractor'
USER_Workforce = 'workforce'
USER_Citizen = 'citizen'
USER_ADMIN = 'admin'
PASSWORD = 'pass'


def create_general_users(self):
    users_data = [
        {'username': USER_STS, 'password': PASSWORD},
        {'username': USER_Landfill, 'password': PASSWORD},
        {'username': USER_Contractor, 'password': PASSWORD},
        {'username': USER_Workforce, 'password': PASSWORD},
        {'username': USER_Citizen, 'password': PASSWORD},
    ]
    for data in users_data:
        username = data['username']
        password = data['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created user: {username} password: {password}'))
        else:
            self.stdout.write(self.style.WARNING(
                f'User {username} already exists. Skipping...'))


def create_super_user(self):
    username = USER_ADMIN
    password = PASSWORD

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Superuser\n\t email:\t\t {username}\n\t password:\t {password}'))
    else:
        self.stdout.write(self.style.WARNING(
            f'User {username} already exists. Skipping...'))
    user, _ = User.objects.get_or_create(username=username, password=password)
    return user


def create_groups(self):
    group_names = [
        settings.GROUP_NAME_SYSTEM_ADMIN,
        settings.GROUP_NAME_STS_MANAGER,
        settings.GROUP_NAME_LANDFILL_MANAGER,
        settings.GROUP_NAME_CONTRACTOR_MANAGER,
        settings.GROUP_NAME_WORKFORCE,
        settings.GROUP_NAME_CITIZEN
    ]
    for group in group_names:
        if not Group.objects.filter(name=group).exists():
            group, created = Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(
                f'Group : {group} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Group : {group} already exists. Skipping...'))


def add_permissions_to_system_admin_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_SYSTEM_ADMIN)

    # Get all available content types (models)
    content_types = ContentType.objects.all()

    # Get all permissions for each model and add them to the system_admin group
    for content_type in content_types:
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)


def add_permissions_to_sts_manager_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_STS_MANAGER)
    content_type = ContentType.objects.get_for_model(WasteTransfer)
    permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.add(*permissions)


def add_permissions_to_landfill_manager_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_LANDFILL_MANAGER)
    content_type = ContentType.objects.get_for_model(WasteTransfer)
    permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.add(*permissions)


def add_user1_to_system_admin_group(self):
    user = User.objects.get(username=USER_STS)
    system_admin_group = Group.objects.get(
        name=settings.GROUP_NAME_SYSTEM_ADMIN)
    user.groups.add(system_admin_group)


def create_vehicles(self):
    cc = 0
    for vehicle in load_vehicle():
        Vehicle.objects.get_or_create(**vehicle)
        cc += 1
    self.stdout.write(self.style.SUCCESS(
        f'Successfully loaded {cc} Vehicle into db...'))


def create_sts(self):
    cc = 0
    return_sts = None
    for sts in load_sts():
        return_sts, _ = STS.objects.get_or_create(**sts)
        cc += 1
    self.stdout.write(self.style.SUCCESS(
        f'Successfully loaded {cc} STS into db...'))
    return return_sts


def create_landfill(self):
    landfill, _ = Landfill.objects.get_or_create(
        address="Amin Bazar Landfill",
        capacity=3500,
        latitude=23.79795912830887,
        longitude=90.30016736544847,
    )
    self.stdout.write(self.style.SUCCESS(
        f'Successfully loaded 1 Landfill into db...'))

    return landfill


def create_sts_manager(self, sts, user):
    STSManager.objects.get_or_create(
        sts=sts, user=user)
    self.stdout.write(self.style.SUCCESS(
        f'Added {user.username} as sts manager '))


def create_landfill_manager(self, landfill, user):
    LandfillManager.objects.get_or_create(
        landfill=landfill, user=user)
    self.stdout.write(self.style.SUCCESS(
        f'Added {user.username} as landfill manager'))


def create_contractor_manager(self, contractor, user):
    ContractorManager.objects.get_or_create(
        contractor=contractor, user=user)
    self.stdout.write(self.style.SUCCESS(
        f'Added {user.username} as contractor manager'))


class Command(BaseCommand):
    help = 'Load Initial Dabatabase'

    def handle(self, *args, **kwargs):
        create_groups(self)
        add_permissions_to_system_admin_group(self)
        # add_permissions_to_sts_manager_group(self)
        # add_permissions_to_landfill_manager_group(self)

        # super_user = create_super_user(self)

        create_system_admin(
            username=USER_ADMIN,
            password=PASSWORD,
        )
        create_general_users(self)

        create_vehicles(self)
        sts = create_sts(self)
        landfill = create_landfill(self)

        create_sts_manager(self, sts, User.objects.get(username=USER_STS))
        create_landfill_manager(
            self, landfill, User.objects.get(username=USER_Landfill))

        contract_contractor_instance = Contract_Contractor.objects.create(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            payment_per_tonnage=100.00,
            required_daily_waste=50.00,
            area_of_collection="Your Area",
            sts=sts
        )
        self.stdout.write(self.style.SUCCESS(
            f'Created contract_contractor_instance'))

        contractor_instance = Contractor.objects.create(
            company_name="ABC Waste Management Company Limited",
            contract=contract_contractor_instance,
            registration_id="1910677111",
            registration_date=date(2024, 1, 1),
            tin="123-456-789-000",
            contact_number="01800112233"
        )
        self.stdout.write(self.style.SUCCESS(
            f'Created contractor_instance'))

        create_contractor_manager(
            self, contractor_instance, User.objects.get(username=USER_Contractor))

        contract_workforce_instance = Contract_Workforce.objects.create(
            start_date=date(2024, 2, 2),
            end_date=date(2024, 12, 31),
            job_title="Van Garbage Collector",
            payment_rate_per_hour=50.00,
            contractor=contractor_instance
        )
        self.stdout.write(self.style.SUCCESS(
            f'Created contract_workforce_instance'))

        workforce_instance = Workforce.objects.create(
            user=User.objects.get(username=USER_Workforce),
            contract=contract_workforce_instance
        )
        self.stdout.write(self.style.SUCCESS(
            f'Created workforce_instance'))
