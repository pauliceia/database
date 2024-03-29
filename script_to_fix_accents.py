#!/usr/bin/env python
# coding: utf-8

from os import makedirs
from os.path import exists

# import pandas as pd
import geopandas as gpd


# path to the original Shapefile
ORIGINAL_SHP = "streets_pilot_area/streets_pilot_area.shp"
# ORIGINAL_SHP = "streets_pilot_area_teste/streets_pilot_area.shp"

# folder path to save the exported Shapefile
FOLDER_TO_SAVE_EXPORTED_SHP = "streets_pilot_area_new"
# file name to save the exported Shapefile
FILE_TO_SAVE_EXPORTED_SHP = "streets_pilot_area.shp"

# file encoding to the exported Shapefile
FILE_ENCODING = 'utf-8'


# acronyms or double words
acronyms = [
    {"old": " dr. ", "new": " doutor "},
    {"old": "dr ", "new": "doutor "},
    {"old": " d. ", "new": " dom "},
    {"old": " cap. ", "new": " capitão "},
    {"old": "av. ", "new": "avenida "},
    {"old": "r. ", "new": "rua "},
    {"old": "vila villa ", "new": "villa "},
    {"old": "beco becco ", "new": "becco "},
    {"old": "viaduto viaducto ", "new": "viaducto "}
]

def fix_acronyms(cell):
    # remove acronyms and add the long word instead

    for acronym in acronyms:
        cell = cell.replace(acronym["old"], acronym["new"])

    return cell


# this function is not needed anymore, because when I save the Shapefile using geopandas, the accents are fixed
def fix_accents(attribute):
    """
    Source: https://stackoverflow.com/a/52905383
    """

    # if attribute is None, then return an empty string
    if attribute is None:
        return ""

    # try to fix the encoding. if fix is not possible, then return the original attribute
    try:
        return attribute.encode("latin-1").decode("raw_unicode_escape").encode("latin-1").decode("utf-8")
    except UnicodeDecodeError:
        return attribute


####################################################################################################
# Read the Shapefile
####################################################################################################

# read file
shapefile = gpd.read_file(ORIGINAL_SHP)


####################################################################################################
# Add new columns and rename someones
####################################################################################################

# Fill "perimeter" column with a default value (i.e. 0)
shapefile["perimeter"] = 0

# Rename "changeset_" column to "changeset_id"
shapefile.rename(columns = {"changeset_": "changeset_id"}, inplace = True)


####################################################################################################
# Add default values by some condition
####################################################################################################

# if there is "NaN" values, then replace them to an empty string
shapefile.loc[shapefile["name"].isnull(), "name"] = ""
# shapefile.loc[shapefile["type"].isnull(), "type"] = ""

# add default "version" and "changeset_id" when they are "0"
shapefile.loc[shapefile["version"] == 0, "version"] = 1
shapefile.loc[shapefile["changeset_id"] == 0, "changeset_id"] = 2

# print("\nshapefile.head(5): \n", shapefile.head(5))
# print("\nshapefile[(shapefile.id == 33) | (shapefile.id == 120)].head(5): \n", shapefile[(shapefile.id == 33) | (shapefile.id == 120)].head(5))
# print("\nshapefile[~(shapefile.obs == "")].head(5): \n", shapefile[~(shapefile.obs == "")].head(5))


####################################################################################################
# Merge "type" with "name" column, in order to remove "type" column
####################################################################################################
"""
# create a new attribute based on name
shapefile["new_name"] = shapefile["name"]

lista = []

for k, linha in shapefile.iterrows():
    if not linha["name"].startswith(linha["type"]):
        lista.append(linha["fid"])

# concatenate "type" with "name" column
shapefile.loc[(shapefile["name"] != "") & (shapefile["fid"].isin(lista)), "new_name"] = shapefile["type"] + " " + shapefile["name"]

# add the value of "new_name" to "name" and delete the old "new_name"
shapefile["name"] = shapefile["new_name"]
del shapefile["new_name"]

# remove unnecessary attributes
if "id_type" in shapefile:
    del shapefile["id_type"]

if "type" in shapefile:
    del shapefile["type"]
"""

####################################################################################################
# Apply a function to the dataframe
####################################################################################################

# print("shapefile.head(15): \n", shapefile.head(15))
# print(shapefile[shapefile.fid==142].name)  
# print(shapefile[shapefile.fid==168].name)  # empty name, but "rua" is added as prefix

# apply "fix_acronyms" function to each cell on my columns
shapefile["name"] = shapefile.name.apply(fix_acronyms)

# apply "fix_accents" function to each cell on my columns
shapefile["name"] = shapefile.name.apply(fix_accents)
shapefile["obs"] = shapefile.obs.apply(fix_accents)


####################################################################################################
# Extra
####################################################################################################

# remove unnecessary attributes
# "perimeter" is necessary to "Edit" portal
# if "perimeter" in shapefile:
#     del shapefile["perimeter"]

# change the columns order
# shapefile = shapefile[["fid", "id", "id_street", "name", "obs", "first_year", "last_year", "perimeter", 
#                        "version", "changeset_id", "geometry"]]
shapefile = shapefile[["id", "id_street", "name", "obs", "first_year", "last_year", "perimeter", 
                       "version", "changeset_id", "geometry"]]


####################################################################################################
# Save the new Shapefile
####################################################################################################

# verify it the folder exists, if it does not exist, then make it
if not exists(FOLDER_TO_SAVE_EXPORTED_SHP):
    makedirs(FOLDER_TO_SAVE_EXPORTED_SHP)

# save result in a file
shapefile.to_file(FOLDER_TO_SAVE_EXPORTED_SHP + "/" + FILE_TO_SAVE_EXPORTED_SHP, encoding=FILE_ENCODING)

# print("\nshapefile.head(5): \n", shapefile.head(5))
print("\nshapefile[...].head(5): \n", 
        shapefile[
            (shapefile.id == 33) | (shapefile.id == 107) | (shapefile.id == 108) | (shapefile.id == 120) | (shapefile.id == 128)
        ].head(5))
# print("\nshapefile[~(shapefile.obs == "")].head(5): \n", shapefile[~(shapefile.obs == "")].head(5))

print("\nIt worked!\n")
