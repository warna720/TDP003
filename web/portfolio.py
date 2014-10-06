#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#This module contains functions related to displaying and handling the webpage

from flask import Flask, render_template, request
import data, random

app = Flask(__name__)


"""Sites_______________________________________________________________________________"""

@app.route('/')
def index():
    randomproject = data.get_random_project(data.load("data.json"))
    return render_template('index.html', project=randomproject)


@app.route('/list', methods=["GET", "POST"])
def projects():
    projects = data.load("data.json")
    if request.method == "GET":
        return render_template('list.html', projectlist=projects, listlength=len(projects))
    elif request.method == "POST":
        searchedlist = data.search(projects, search=request.form["searchstr"])
        return render_template('list.html', projectlist=searchedlist, listlength=len(searchedlist))


@app.route('/project/<int:project_id>')
def get_project_id(project_id):
    projectlist = data.load("data.json")
    retrivedproject = data.get_project(projectlist, project_id)
    return render_template('project.html', project=retrivedproject)


@app.route('/techniques')
def techniques():
    projects = data.load("data.json")
    retrived_techniques = data.get_technique_stats(projects)
    return render_template('techniques.html', techs=retrived_techniques, keys=retrived_techniques.keys())


@app.route('/search', methods=["GET", "POST"])
def search():
    projects = data.load("data.json")
    retrived_techniques = data.get_technique_stats(projects)
    if request.method == "GET":
        return render_template('search.html', keys=retrived_techniques.keys())

    elif request.method == "POST":
        searchfields = request.form.getlist("searchfields")
        if len(searchfields) == 0:
            searchfields = None
        foundprojects = data.search(projects, sort_by=request.form.getlist("sortby")[0], sort_order=request.form.getlist("sortorder")[0], techniques=request.form.getlist("techniques"), search=request.form.getlist("searchstr")[0], search_fields=searchfields)
        return render_template('search.html', keys=retrived_techniques.keys(), projectlist=foundprojects, matches=len(foundprojects))




"""Error handling______________________________________________________________________"""

@app.errorhandler(500)
def internal_server_error(error):
    """Internal Server Error"""
    return 'Internal Server Error<br>%s' % error

@app.errorhandler(400)
def bad_request(error):
    """Bad request"""
    return 'Bad request<br>%s' % error

@app.errorhandler(404)
def page_not_found(error):
    """Page not found"""
    return 'No Harald Here<br>%s' % error

if __name__ == '__main__':
    app.run()
