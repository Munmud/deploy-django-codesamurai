import os
import random
# from tqdm import tqdm
import json
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from core.utils import load_sts, load_vehicle, aws_map_route_api
from waste.models import *


class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        sts = get_object_or_404(STS, id=1)
        landfill = get_object_or_404(Landfill, id=1)
        OptimizeForList = ['FastestRoute', 'ShortestRoute']
        print(sts, landfill)
        for OptimizeFor in OptimizeForList:
            if Path.objects.filter(
                sts=sts,
                landfill=landfill,
                OptimizeFor=OptimizeFor
            ).exists():
                return
            res = aws_map_route_api(
                source_lat=sts.latitude,
                source_lon=sts.longitude,
                dest_lat=landfill.latitude,
                dest_lon=landfill.longitude,
                OptimizeFor=OptimizeFor
            )
            print(sts, landfill, OptimizeFor, type(res))

        #         DriveDistance = res['DriveDistance']
        #         DistanceUnit = res['DistanceUnit']
        #         DriveTime = res['DriveTime']
        #         TimeUnit = res['TimeUnit']
        #         PathList = json.dumps({"PathList": res['PathList']})
        #         path, created = Path.objects.get_or_create(
        #             sts=sts,
        #             landfill=landfill,
        #             OptimizeFor=OptimizeFor,
        #             DriveDistance=DriveDistance,
        #             DistanceUnit=DistanceUnit,
        #             DriveTime=DriveTime,
        #             TimeUnit=TimeUnit,
        #             points=PathList
        #         )


#
