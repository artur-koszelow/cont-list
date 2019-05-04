from flask import Flask, request, jsonify
import github
import json

app = Flask(__name__)

# Create GitHub instance to menage GitHub resources
g = github.Github('d182396a7a87608bbe39d24a17766a830cf8cf0f')

@app.route("/")
def main_page():
    return 'Hello ;)<br/>\
    <br/>\
    API is accessed from local host <b>(127.0.0.1:5000)</b> and data is received as <b>JSON</b><br/>\
    <br/>\
    To fetch the list of all contributors sorted by the number of contributions made by developer to all\
    repositories for the given organization:<br/>\
    <br/>\
    <b>GET /org/:organisation</b><br/>\
    <br/>\
    <b>e.g. 127.0.0.1:5000/org/adobe</b><br/>\
    <br/>\
    When organisation have lot or repositories than application need some\
    time to get all contributors and for now I did not find better way to improve performance.\
    But if you want to check organisations like google than I suggest to reduce number of repositories to \
    less than 160: <br/>\
    <br/>\
    <b>Parameters:</b><br/>\
    <br/>\
    <b>?Start = # </b> List contributors from # repository of given organisation<br/>\
    <br/>\
    <b>?Stop = # </b> List contributors to # repository of given organisation<br/>\
    <br/>\
    <b>e.g. 127.0.0.1:5000/org/google?start=0&stop=160</b><br/>'


@app.route('/org/<string:organisation>')
def get_contributors_list(organisation):

    # Check if organisation exist
    try:
        org = g.get_organization(organisation)
    except github.GithubException:
        return f'Please ;P Of course there is no organisation named <b>"{organisation}"</b>'

    # Grab organisation without repository
    try:
        repos = org.get_repos()
    except github.GithubException:
        return f"organisation {organisation} don't have any repository"


    # Iterate through repositories of given organisation to collect unsorted list of contributors
    pre_list = {}

    # Some of repositories have countless contributors and We will grab those to error dict
    errors = {}

    # Organisation such as Google have a huge amount of repositories so here we can specify
    # just a part of them
    start = request.args.get('start')
    stop = request.args.get('stop')
    if start is None:
        start = 0
    if stop is None:
        stop = 999999
    elif int(stop) <= int(start):
        return 'Stop value must be larger than start'

    # Get list of contributors and contributions that they make in whole organisation
    # And also grab that repositories with countless contributors
    for repo in repos[int(start):int(stop)]:
        try:
            contributors = repo.get_contributors()
            for contributor in contributors:
                if contributor.login not in pre_list:
                    pre_list[contributor.login] = contributor.contributions
                else:
                    pre_list[contributor.login] += contributor.contributions

        except github.GithubException as e:
            errors[repo.name] = e.data['message']

    # Sort list by number of contributions in descending order & add errors at the end of it if exist
    sort_list = {}
    if len(pre_list) > 0:
        names, values = zip(*sorted(pre_list.items(), key=lambda kv: kv[1], reverse=True))
        for _ in range(len(names)):
            sort_list[names[_]] = values[_]
    if len(errors) > 0:
        sort_list['Errors'] = errors

    # create JSON response
    response = app.response_class(
        response=json.dumps(sort_list, indent=2),
        status=200,
        mimetype='application/json')

    return response


@app.route('/org')
def too_short():
    orgs_list = []
    orgs = g.get_organizations()
    for org in orgs[:15]:
        orgs_list.append(org.login)
    return jsonify(['Specify the name of organisation after forward slash'], {'some examples': orgs_list})


@app.errorhandler(404)
def page_error(e):
    return "Nope. Nothing to do here ;) Maybe try:<br/><b>127.0.0.1:5000/org/google?start=81&stop=83<b/>"


if __name__ == '__main__':
    app.run(debug=True)
