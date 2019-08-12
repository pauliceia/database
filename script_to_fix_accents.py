#!/usr/bin/env python
# coding: utf-8

from os import makedirs
from os.path import exists

import pandas as pd
import geopandas as gpd


DIR_ORIGINAL_SHP = "streets_pilot_area/streets_pilot_area.shp"

FOLDER_TO_SAVE_SHP = "streets_pilot_area_new"
FILE_TO_SAVE_SHP = "streets_pilot_area.shp"


acronyms = [
    {"old": " dr. ", "new": " doutor "},
    {"old": "dr ", "new": "doutor "},
    {"old": " d. ", "new": " dom "},
    {"old": " cap. ", "new": " capitão "},
    {"old": "av. ", "new": "avenida "},
    {"old": "r. ", "new": "rua "},
    {"old": "vila villa ", "new": "villa "}
]

def fix_acronyms(cell):
    # remove acronyms and add the long word instead

    for acronym in acronyms:
        cell = cell.replace(acronym["old"], acronym["new"])

    return cell


# this function is not needed anymore, because when I save the Shapefile using geopandas, the accents are fixed
# def fix_accents(attribute):
#     if attribute is None:
#         return ""

#     return attribute.encode('latin-1').decode('raw_unicode_escape').encode('latin-1').decode('utf-8')


# shape['name'] = shape.name.apply(fix_accents)

# read file
shapefile = gpd.read_file(DIR_ORIGINAL_SHP)

# if there is NaN values, then replace them to empty string
shapefile.loc[shapefile['name'].isnull(), 'name'] = ""
shapefile.loc[shapefile['type'].isnull(), 'type'] = ""

# print("shape.head(15): \n", shape.head(15))
# print(shapefile[shapefile.fid==142].name)
# print(shapefile[shapefile.fid==168].name)

# create a new attribute based on name
shapefile['new_name'] = shapefile['name']

lista = []

for k, linha in shapefile.iterrows():
    if not linha['name'].startswith(linha['type']):
        lista.append(linha['fid'])

shapefile.loc[(shapefile['name'] != "") & (shapefile['fid'].isin(lista)), 'new_name'] = shapefile['type'] + ' ' + shapefile['name']

# add the value of 'new_name' to 'name' and delete the old 'new_name'
shapefile['name'] = shapefile['new_name']
del shapefile['new_name']

# print("shape.head(15): \n", shape.head(15))
# print(shapefile[shapefile.fid==142].name)  
# print(shapefile[shapefile.fid==168].name)  # empty name, but 'rua' is added as prefix

# apply the 'fix_acronyms' function to each cell on my 'name' column
shapefile['name'] = shapefile.name.apply(fix_acronyms)


# remove unnecessary attributes
if 'id_type' in shapefile:
    del shapefile['id_type']

if 'type' in shapefile:
    del shapefile['type']

if 'perimeter' in shapefile:
    del shapefile['perimeter']


# verify it the folder exists, if it does not exist, then make it
if not exists(FOLDER_TO_SAVE_SHP):
    makedirs(FOLDER_TO_SAVE_SHP)

# save result in a file
shapefile.to_file(FOLDER_TO_SAVE_SHP + "/" + FILE_TO_SAVE_SHP)

print("It worked!")
