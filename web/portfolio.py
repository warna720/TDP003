#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#This module contains functions related to displaying and handling the webpage

from flask import Flask, render_template, request, abort
import data

app = Flask(__name__)

"""Sites_______________________________________________________________________________"""

@app.route('/')
def index():
    data.logger("Request", request.method, "/")
    randomproject = data.get_random_project(data.load("data.json"))
    data.logger("Success")
    return render_template('index.html', project=randomproject)


@app.route('/list', methods=["GET", "POST"])
def projects():
    data.logger("Request", request.method, "/list")
    projects = data.load("data.json")
    #Sort list based on project id
    projects = data.search(projects, sort_by='project_no', sort_order='asc')

    if request.method == "GET":
        data.logger("Success")
        return render_template('list.html', projectlist=projects, listlength=len(projects))
    elif request.method == "POST":
        small_search_fields = data.possible_fields[:]
        small_search_fields.remove("small_image")
        small_search_fields.remove("big_image")
        searchedlist = data.search(projects, search=request.form["searchstr"], search_fields=small_search_fields)
        data.logger("Success")
        return render_template('list.html', projectlist=searchedlist, listlength=len(searchedlist))


@app.route('/project/<int:project_id>')
def get_project_id(project_id):
    data.logger("Request", request.method, "/project/"+str(project_id))
    projectlist = data.load("data.json")
    retrivedproject = data.get_project(projectlist, project_id)
    if not retrivedproject:
        abort(404)
    data.logger("Success")
    return render_template('project.html', project=retrivedproject)


@app.route('/techniques')
def techniques():
    data.logger("Request", request.method, "/techniques")
    projects = data.load("data.json")
    retrived_techniques = data.get_technique_stats(projects)
    data.logger("Success")
    return render_template('techniques.html', techs=retrived_techniques, keys=retrived_techniques.keys())


@app.route('/search', methods=["GET", "POST"])
def search():
    data.logger("Request", request.method, "/search")
    projects = data.load("data.json")
    retrived_techniques = data.get_technique_stats(projects)
    if request.method == "GET":
        data.logger("Success")
        return render_template('search.html', keys=retrived_techniques.keys())

    elif request.method == "POST":
        searchfields = request.form.getlist("searchfields")
        if len(searchfields) == 0:
            searchfields = None
        foundprojects = data.search(projects, sort_by=request.form.getlist("sortby")[0], sort_order=request.form.getlist("sortorder")[0], techniques=request.form.getlist("techniques"), search=request.form.getlist("searchstr")[0], search_fields=searchfields)
        data.logger("Success")
        return render_template('search.html', keys=retrived_techniques.keys(), projectlist=foundprojects, matches=len(foundprojects))


"""Error handling______________________________________________________________________"""

@app.errorhandler(500)
def internal_server_error(error):
    """Internal Server Error"""
    message = "Internal Server Error!"
    data.logger("Internal server error", str(error))
    return render_template('error.html', error = error, message = message)

@app.errorhandler(400)
def bad_request(error):
    """Bad request"""
    message = "Bad request!"
    data.logger("Bad request", str(error))
    return render_template('error.html', error = error, message = message)

@app.errorhandler(404)
def page_not_found(error):
    """Page not found"""
    message = "The page was not found!"
    data.logger("Page not found", str(error))
    return render_template('error.html', error = error, message = message)

if __name__ == '__main__':
    app.run()
