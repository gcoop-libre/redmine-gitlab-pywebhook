#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask_ini import FlaskIni
from flask import Flask, jsonify, abort
from werkzeug.contrib.fixers import ProxyFix
from flask import make_response
from flask import request
from redmine import Redmine
from regex import match, IGNORECASE

app = Flask(__name__)

app.iniconfig = FlaskIni()
with app.app_context():
    app.iniconfig.read('config.ini')

#http://www.redmine.org/projects/redmine/wiki/Rest_api_with_python

@app.route('/redmine.json', methods=['POST', 'GET'])
def redmine():
    if not request.json:
        print 'Falta datos en el json: ' + str(request.json)
        abort(400, 'Falta datos en el json: ' + str(request.json))

    api_key = app.iniconfig.get('redmine', 'api_key')
    url = app.iniconfig.get('redmine', 'url')
    #"commits": [
    #  {
    #    "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
    #    "message": "Update Catalan translation to e38cb41.",
    #    "timestamp": "2011-12-12T14:27:31+02:00",
    #    "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
    #    "author": {
    #      "name": "Jordi Mallach",
    #      "email": "jordi@softcatala.org"
    #    }
    #  },
    #  {
    #    "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
    #    "message": "fixed readme",
    #    "timestamp": "2012-01-03T23:36:29+02:00",
    #    "url": "http://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
    #    "author": {
    #      "name": "GitLab dev user",
    #      "email": "gitlabdev@dv6700.(none)"
    #    }
    #  }
    #],
    #"total_commits_count": 4
    redmine = Redmine(url, key=api_key, requests={'verify': False})
    request.json['commits'].reverse()
    branch = request.json['ref'].split('/')[2]
    default_branch = request.json['project']['default_branch']
    note = ''
    if branch == default_branch:
        for commit in request.json['commits']:
            m = match('(rel|issue|fix|fixes)\s*#?(\d+)', commit['message'],
                    IGNORECASE)
            if m is not None:
                accion = m.groups()[0].lower()
                status = None
                note = '<pre>author: ' + commit['author']['name'] + ' <'+commit['author']['email']+'>\n' + \
                    'msg: '+commit['message'] + '</pre>' + 'commit: "' + commit['id'][:8] + '":' + commit['url']
                if accion in('fix', 'fixes'):
                    status = 3  # fix
                    redmine.issue.update(m.groups()[1], notes=note, status_id=status, done_ratio=100)
		else:
                    redmine.issue.update(m.groups()[1], notes=note, status_id=status)

    data = {'msg': 'OK'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': error.description}), 400)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    host = app.iniconfig.get('redmine', 'host', fallback='localhost')
    port = app.iniconfig.getint('redmine', 'port', fallback=5000)

    app.run(host=host, port=port, debug=True)
