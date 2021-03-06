from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
	return """
Available API endpoints:

GET /containers List all containers
GET /containers?state=running List running containers (only)
GET /containers/&lt;id&gt; Inspect a specific container
GET /containers/&lt;id&gt;/logs Dump specific container logs
GET /images List all images

POST /images Create a new image
POST /containers Create a new container

PATCH /containers/<id> Change a container's state
PATCH /images/<id> Change a specific image's attributes

DELETE /containers/<id> Delete a specific container
DELETE /containers Delete all containers (including running)
DELETE /images/<id> Delete a specific image
DELETE /images Delete all images

"""
def docker(*args):
cmd = ['docker']
for sub in args:
cmd.append(sub)
process = Popen(cmd, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
if stderr.startswith('Error'):
print 'Error: {0} -&gt; {1}'.format(' '.join(cmd),
stderr)
return stderr + stdout

#
# Docker output parsing helpers
#

#
# Parses the output of a Docker PS command to a python List
#
def docker_ps_to_array(output):
all = []
for c in [line.split() for line in
output.splitlines()[1:]]:
each = {}
each['id'] = c[0]
each['image'] = c[1]
each['name'] = c[-1]
each['ports'] = c[-2]
all.append(each)
return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
logs = {}
logs['id'] = id
all = []
for line in output.splitlines():
all.append(line)
logs['logs;' = all
return logs

#
# Parses the output of a Docker image command to a pythonList
#
def docker_images_to_array(output):
all = []
for c in [line.split() for line in
output.splitlines()[1:]]:
each = {}
each['id'] = c[2]
each['tag'] = c[1]
each['name'] = c[0]
all.append(each)
return all
@app.route('/containers', methods=['GET'])
# define an endpoint to list all containers
def containers_index():
"""
List all containers
curl -s -X GET -H 'Accept: application/json'
http://localhost:8080/containers | python -mjson.tool
curl -s -X GET -H &#39;Accept: application/json&#39;
http://localhost:8080/containers?state=running | python -
mjson.tool

"""
if request.args.get('state') == 'running':
output = docker('ps')
else:
output = docker('ps', '-a')
resp = json.dumps(docker_ps_to_array(output))
return Response(response=resp,
mimetype="application/json")
