from geopy.distance import geodesic
import itertools
import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import os
import csv
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
import time

STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")
VEHICLE_METADATA_CSV = os.path.join(settings.DATA_DIR, "vehicle.csv")
NEIGHBOURHOOD_METADATA_CSV = os.path.join(
    settings.DATA_DIR, "neighbourhood.csv")


def generate_schedule(number_of_neighbourhood=3, number_of_van=2, neighbors=[[10, 1, 1], [2, 39, -70], [3, 5, 7]], sts=(0, 0)):
    """
    # input neighbors=[[10,1,1],[...],....]  
        here [[id,latitude,longitude],....]

    # output two object result, path_result.  
        result[i]=[van number, neighbor id, finish time], 
        path_result[i]= optimized path for van i.
    """
    index = []
    locations = []

    def distance(location1, location2):
        # Calculate distance using geodesic distance between two latitude and longitude coordinates
        return geodesic(location1, location2).kilometers

    # Function to solve the Traveling Salesman Problem using the Held-Karp algorithm

    def tsp_held_karp(locations):
        n = len(locations)
        G = nx.complete_graph(n)  # Complete graph with locations as nodes

        # Calculate distances between all pairs of locations
        for i in range(n):
            for j in range(n):
                if i != j:
                    G[i][j]['weight'] = distance(locations[i], locations[j])

        # Generate all permutations of locations with the last location fixed at the end
        permutations = itertools.permutations(range(n - 1))

        # Initialize minimum distance and path
        min_distance = float('inf')
        min_path = None

        # Iterate over all permutations and calculate total distance
        for perm in permutations:
            # Add the last location to the end of the permutation
            perm_with_last = perm + (n - 1,)
            total_distance = 0
            for i in range(n - 1):
                total_distance += G[perm_with_last[i]
                                    ][perm_with_last[i + 1]]['weight']
    #         total_distance += G[perm_with_last[-1]][perm_with_last[0]]['weight']  # Add distance back to the starting location
            if total_distance < min_distance:
                min_distance = total_distance
                min_path = perm_with_last

        return min_path

    def cluster_locations(locations, m):
        X = np.array(locations)
        kmeans = KMeans(n_clusters=m, random_state=0).fit(X)
        return kmeans.labels_

    def generate_clusters(locations, m):
        labels = cluster_locations(locations, m)
        clusters = [[] for _ in range(m)]
        for i, label in enumerate(labels):
            clusters[label].append(i)

        return clusters

    for i in range(number_of_neighbourhood):
        index.append(neighbors[i][0])
        locations.append((neighbors[i][1], neighbors[i][2]))

    clusters = generate_clusters(locations, number_of_van)

    result = []
    path_result = []

    van_number = 1
    for cluster in clusters:
        time = 9
        length = len(cluster)

        loc = []
        for i in range(length):
            loc.append(locations[cluster[i]])
        loc.append(sts)
        path = tsp_held_karp(loc)

        prow = []
        rrow = []
        plen = len(path)

        for x in range(plen-1):
            ind = index[cluster[path[x]]]
            prow.append(ind)
            rrow = []
            rrow.append(van_number)
            rrow.append(ind)
            rrow.append(time)
            time = time+1
            result.append(rrow)

        # prow.append("sts")
        path_result.append(prow)
        van_number += 1

    return result, path_result


def create_system_admin(username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password=password)
        group, created = Group.objects.get_or_create(name='System Admin')
        user.groups.add(group)
        user.is_staff = True
        user.save()
        print(f"User '{username}' is now a system admin.")


def is_system_admin(user):
    return user.groups.filter(name=settings.GROUP_NAME_SYSTEM_ADMIN).exists()


def is_sts_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_STS_MANAGER).exists()


def is_landfill_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_LANDFILL_MANAGER).exists()


def is_contractor_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_CONTRACTOR_MANAGER).exists()


def is_workforce(user):
    return user.groups.filter(name=settings.GROUP_NAME_WORKFORCE).exists()


def is_citizen(user):
    return user.groups.filter(name=settings.GROUP_NAME_CITIZEN).exists()


def load_sts():
    dataset = []
    with open(STS_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            data = {
                'ward':  int(row.get("ward")),
                'capacity':  int(row.get("capacity")),
                'zone':  int(row.get("zone")),
                'address': row.get("address"),
                'latitude':  row.get("latitude"),
                'longitude':  row.get("longitude"),
            }
            dataset.append(data)
    return dataset


def load_vehicle():
    dataset = []
    with open(VEHICLE_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            data = {
                'vehicle_number': row.get("vehicle_number"),
                'type': row.get("type"),
                'capacity': int(row.get("capacity")),
                'loaded_fuel_cost_per_km':  float(row.get("loaded_fuel_cost_per_km")),
                'unloaded_fuel_cost_per_km': float(row.get("unloaded_fuel_cost_per_km"))
            }
            dataset.append(data)
            # print(data)
            # break
    return dataset


def load_neighbourhood():
    dataset = []
    with open(NEIGHBOURHOOD_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'name': row.get("name"),
                'latitude':  row.get("latitude"),
                'longitude':  row.get("longitude"),
            }
            dataset.append(data)
    return dataset


def aws_map_route_api(source_lat, source_lon, dest_lat, dest_lon, OptimizeFor):
    api_url = 'https://skay3kwtcg.execute-api.ap-south-1.amazonaws.com/Prod/route'
    payload = {
        "source_lat": source_lat,
        "source_lon": source_lon,
        "dest_lat": dest_lat,
        "dest_lon": dest_lon,
        "optimize_for": OptimizeFor
    }

    max_retries = 2
    retry_delay = 2  # in seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, json=payload).json()
            # print(response)
            data = json.loads(response['data'][0])
            return data         # dict of  DriveDistance, DistanceUnit, DriveTime, TimeUnit, PathList
            break  # If successful, exit the loop
        except Exception as e:
            if attempt < max_retries - 1:
                print(
                    f"Attempt {attempt + 1} failed. Retrying after {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries exceeded. Request failed.")
                print(e)
                # Handle the error or raise it
