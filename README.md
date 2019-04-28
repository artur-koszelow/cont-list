Hello ;)

This script is written in PYTHON language and use FLASK & PyGitHub library. It's use GitHub API to list every contributors sorted by the number of contributions made by developer to all repositories for the given organization.

API is accessed from local host (127.0.0.1:5000) and data is received as JSON

GET /org/:organisation

e.g. 127.0.0.1:5000/org/adobe

When organisation have lot or repositories than application need some time to get all contributors and for now I did not find better way to improve performance. If you want to check organisations like google than I suggest to reduce number of repositories to less than 160:

Parameters:

?start = # -> List contributors from # repository of given organisation

?stop = # -> List contributors to # repository of given organisation

e.g. 127.0.0.1:5000/org/google?start=0&stop=160