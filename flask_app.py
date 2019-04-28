from flask import Flask
from github import Github
import json

app = Flask(__name__)


@app.route("/")
def main_page():
    return 'Hello Scala ;)<br/>\
    <br/>\
    Welcome to my first ever project where I worked with API :)\
    It is difficult to handle new objective in 3 days but I hope that I make your assignment right\
    in part of your criteria.<br/> When organisation have lot or repositories than application need some\
    time to get all contributors and for now I did not find better way to improve performance.<br/>\
    <br/>\
    API is accessed from local host (127.0.0.1:5000) and data is received as JSON<br/>\
    <br/>\
    To fetch the list of all contributors sorted by the number of contributions made by developer to all\
    repositories for the given organization:<br/>\
    <h3>GET /org/:organisation</h3><br/>\
    <br/>\
    e.g. 127.0.0.1:5000/org/adobe'


@app.route('/org/<string:organisation>')
def get_contributors_list(organisation):

    # Create GitHub instance to menage GitHub resources
    g = Github('d182396a7a87608bbe39d24a17766a830cf8cf0f')
    org = g.get_organization(organisation)
    repos = org.get_repos()

    # Iterate through repositories of given organisation to collect unsorted list of contributors
    pre_list = {}
    for repo in repos:
        for contributor in repo.get_contributors():
            if contributor.login not in pre_list:
                pre_list[contributor.login] = contributor.contributions
            else:
                pre_list[contributor.login] += contributor.contributions

    # Sort list by number of contributions in descending order
    names, values = zip(*sorted(pre_list.items(), key=lambda kv: kv[1], reverse=True))

    sort_list = {}
    for _ in range(len(names)):
        sort_list[names[_]] = values[_]

    # create JSON response
    response = app.response_class(
        response=json.dumps(sort_list, indent=2),
        status=200,
        mimetype='application/json')

    return response


if __name__ == '__main__':
    app.run(debug=True)
