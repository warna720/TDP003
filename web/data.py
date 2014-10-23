#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#This module contains functions that are meant to handle project data
#stored in .json files

import json, datetime, random

#Global list containing the required project fields. Used in the search function, and is global so it doesn't have to be recreated once every time search is called.
possible_fields = ["project_no", "project_name", "start_date", "end_date", "course_id", "course_name", "techniques_used", "short_description", "long_description", "small_image", "big_image", "external_link", "academic_credits"]

def logger(functionname, *args):
    """This function writes info to a log file (log.txt) about functions 
       that have been called.

       Parameters:
         functionname: A string containing the name of the function
         *args: Strings containing the arguments passed to the function"""

    now = datetime.datetime.now()
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "T" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "+01:00 " + functionname)
        for a in args:
            f.write(", " + str(a))
        f.write("\n"*2)

    f.close()

def load(filename):
    """This function reads a .json file, and returns the content of the file
       in a list.

       Parameters:
         filename: The name of the .json file as a string"""

    logger("load", "filename="+str(filename))


    try:
        db = json.load(open(filename, 'r', encoding = 'utf-8'))
        for project in db:
            #Make sure that there is no techniques duplicates because of case sensitive.
            unique_list = []
            for tech in project['techniques_used']:
                if tech.lower() not in unique_list:
                    unique_list.append(tech.lower())
            project["techniques_used"] = unique_list

        #Fix invalid url for images. Problem occurs when image link is not local.
        db = fix_images_url(db)

        return db
    except:
        return None

def get_random_project(db):
    """Returns a random project from given list"""
    randomproject = random.choice(db)
    logger("get_random_project", "db=data.json", "random_project_no="+str(randomproject['project_no']))
    return randomproject


def get_project_count(db):
    """This function returns the number of projects in a list of
       projects.

       Parameters:
         db: A list of projects as returned by load(filename)"""

    logger("get_project_count", "db=data.json")

    return len(db)


def get_project(db, id):
    """This function fetches a project with a specific id from a list
       of projects.

       Parameters:
         db: A list of projects as returned by load(filename)
         id: The ID number of the project you want to get"""

    logger("get_project", "id="+str(id), "db=data.json")

    for project in db:
        if project["project_no"] == id: return project
    return None

def fix_images_url(db):
    for project in db:
        if not "http://" in project["big_image"]:
            project["big_image"] = "/static/images/" + project["big_image"]

        if not "http://" in project["small_image"]:
            project["small_image"] = "/static/images/" + project["small_image"]

    return db


def search(db, sort_by="start_date", sort_order="desc", techniques=None, search=None, search_fields=None):
    """This function fetches and sorts projects matching criteria from
       the specified list of projects. It returns a list of dictionaries
       for all projects conforming to the specified search criteria.

       Parameters:
         db: A list of projects as returned by load(filename)
         sort_by: A string containing the name of the field to sort by
         sort_order: A string containing the order to sort in, can
                     either be "asc" for ascending, or "desc" for
                     descending
         techniques: A list of techniques that projects must have to be
                     returned. An empty list means the field is ignored
         search: A string containing a free text search string
         search_fields: A list of fields to search for the parameter search
                        in. If search_fields is empty, no results are returned.
                        If search_fields is None, all fields are searched."""

    logger("search", "db=data.json", "sort_by="+str(sort_by), "sort_order="+str(sort_order), "techniques="+str(techniques), "search="+str(search), "search_fields="+str(search_fields))

    if search_fields == []: return []

    matches = []

    #If no search_fields provided, get all fields for searching.
    if not search_fields: search_fields = possible_fields

    #If search provided
    if search and search.strip():
        search = search.strip()
        #HOTFIX - If multiple words given, just use first word
        search = str(search).split()[0]
        for project in db:
            for field in search_fields:
                #If match.
                if field in project.keys() and search.lower() in str(project[field]).lower():
                    matches.append(project)
    else:
        matches = db

    #If techniques provided
    if techniques:
        matches = [project for project in matches for tech in project['techniques_used'] if tech in techniques]

    #Remove any duplicates
    matches = list({v["project_no"]:v for v in matches}.values())

    if sort_order == "asc":
        matches.sort(key = lambda l: l[sort_by])
    elif sort_order == "desc":
        matches.sort(key = lambda l: l[sort_by], reverse = True)

    return matches


def get_techniques(db):
    """This function fetches a list of all techniques alphabetically
       sorted from a list of projects.

       Parameters:
         db: A list of projects as returned by load(filename)"""

    logger("get_techniques", "db=data.json")

    techniques = []

    #Inserts the techniques of every project into techniques.
    for project in db:
        techniques.extend(project["techniques_used"])

    #Converts to set (unique left), back to list and sorts it.
    return sorted(list(set(techniques)))


def get_technique_stats(db):
    """This function collects statistics for all techniques in a list of
       projects, and returns a dictionary, where the key is the name of a
       technique, and the value is a list of dictionaries that contains
       the following keys and values:
         id: Project number
         name: Name of the project

       Parameters:
         db: A list of projects as returned by load(filename)"""

    logger("get_technique_stats", "db=data.json")

    #Add every tech to dict with value as empty list.
    techniques = {key : [] for key in get_techniques(db)}

    for tech in techniques:
        for project in db:
            if tech in project["techniques_used"]:

                #Add to techniques dict to corresponding technique.
                techniques[tech] += [{"id" : project["project_no"], "name" : project["project_name"]}]


    for tech in techniques:
        #Sort dicts inside list based on value of name.
        techniques[tech].sort(key = lambda l: l["name"])

    return techniques
