from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

import requests
import logging
import base64
import json

app = Flask(__name__)

## TODO: Local all configuration from a config file
githubConfig = {
  'stack': {
    'org': "cardinrich",
    'repo': "githubtest"
  },
  'pipeline': {
    'org': "cardinrich",
    'repo': "githubtest"
  },
  'environment': {
    'org': "cardinrich",
    'repo': "envstore"
  },
  'testing': {
    'org': "cardinrich",
    'repo': "new"
  }
}

def isValidRoute(route):
  if route in githubConfig.keys():
    return True

def getGithubOrg(route):
  return githubConfig[route]['org']

def getGithubRepo(route):
  return githubConfig[route]['repo']

gitUser = "Richcardin"
gitPass = "c7c0591e5bc146e32aec51b5d787fce4d6b26ef5"

gitOrg = "cardinrich"
gitRepo = "new"
gitRepo = "githubtest"

## TODO: Dynamic Config
gitCommitterName  = "Richcardin"
gitCommitterEmail = "rcardin27011996@gmail.com"

def _listFiles(route):
  gitContentUrl = "https://api.github.com/repos/" + \
                  getGithubOrg(route) + "/" + \
                  getGithubRepo(route) + "/contents/"

  req = requests.get( gitContentUrl,
                      auth = (gitUser, gitPass))

  if req.status_code != 200:
    logging.warning("status: " + str(req.status_code))
    logging.warning("error msg: " + req.text)
    response = jsonify ( {'status': req.status_code, 'error': req.text} )
    response.status_code = req.status_code
    return response
  data = req.json()
  logging.warning(json.dumps(data, indent=2))

  filearr=[]
  for index in range(len(data)):
    filearr.append ({"name": data[index]['name'],
                     "type": data[index]['type'],
                     "size": data[index]['size'],
                     "sha" : data[index]['sha']})

  return jsonify(filearr)

def _getFile(route, filename):
   gitContentUrl = "https://api.github.com/repos/" + \
                  getGithubOrg(route) + "/" + \
                  getGithubRepo(route) + "/contents/" + \
                  filename
   req = requests.get( gitContentUrl,
                      auth = (gitUser, gitPass))

   if req.status_code !=200:
     logging.warning("status : " + str(req.status_code))
     logging.warning(json.dumps(req.text, indent=2))
     response = jsonify ( {'status': req.status_code, 'error': "could not retrieve sha"} )
     response.status_code = req.status_code
     return response

   data = req.json()
  
   content = base64.b64decode(data['content']).decode('utf-8')
   payload = {"filename": data['name'],
              "sha": data['sha'],
              "content": content}
   return jsonify(payload)
  
def _createFile(route, filename, data):
      
      content = base64.b64encode(json.dumps(data, indent=2))
      payload = { 'message': 'automated update', 'committer': { 'name': gitCommitterName, 'email': gitCommitterEmail}, 'content': content}
      logging.warning(json.dumps(payload, indent=2))

      gitContentUrl = "https://api.github.com/repos/" + \
                  getGithubOrg(route) + "/" + \
                  getGithubRepo(route) + "/contents/"
      
      req = requests.put( gitContentUrl + filename,
                      auth = (gitUser, gitPass),
                      json = payload)
     
      logging.warning("url: " + gitContentUrl + filename)
      logging.warning("status: " + str(req.status_code))
      logging.warning(json.dumps(req.text, indent=2))

      if req.status_code == 201:
         response = jsonify ( {
                  'status': req.status_code,
                  'msg': "file " + filename + " created",
                  'sha': req.json()['content']['sha']
                  } )
         response.status_code = req.status_code

      if req.status_code == 422:
         response = jsonify ( {'status': req.status_code, 'error': "file " + filename + " already exists"} )
         response.status_code = req.status_code
         return response

      response = jsonify ( {'status': req.status_code, 'error': req.text} )
      response.status_code = req.status_code
      return response

def _updateFile(route, filename, data):
  

   gitContentUrl = "https://api.github.com/repos/" + \
                  getGithubOrg(route) + "/" + \
                  getGithubRepo(route) + "/contents/" + \
                  filename

   req = requests.get( gitContentUrl, auth = (gitUser, gitPass))


   content = base64.b64encode(json.dumps(data, indent=2))
   payload = {'message': 'automated update', 'committer': { 'name': gitCommitterName, 'email': gitCommitterEmail}, 'content': content, 'sha': req.json()['sha']}
   logging.warning(json.dumps(payload, indent=2))


   req = requests.put( gitContentUrl ,
                      auth = (gitUser, gitPass),
                      json = payload)

   logging.warning("url: " + gitContentUrl + filename)
   logging.warning("status: " + str(req.status_code))
   logging.warning(json.dumps(req.text, indent=2))
   
   if req.status_code == 200:
      response = jsonify ( {
                  'status': req.status_code,
                  'msg': "file " + filename + " updated",
                  'sha': req.json()['content']['sha']
                  } )
      response.status_code = req.status_code
      return response

   if req.status_code == 422:
      response = jsonify ( {'status': req.status_code, 'error': "file " + filename + " already exists"} )
      response.status_code = req.status_code
      return response

   response = jsonify ( {'status': req.status_code, 'error': req.text} )
   response.status_code = req.status_code
   return response

  
def _deleteFile(route, filename):
  gitContentUrl = "https://api.github.com/repos/" + \
                  getGithubOrg(route) + "/" + \
                  getGithubRepo(route) + "/contents/" + \
                  filename

  req = requests.get( gitContentUrl,
                      auth = (gitUser, gitPass))

  if req.status_code != 200:
    logging.warning("status: " + str(req.status_code))
    logging.warning(json.dumps(req.text, indent=2))
    response = jsonify ( {'status': req.status_code, 'error': "could not retrieve sha"} )
    response.status_code = req.status_code
    return response

  payload = { 'message': 'automated upload',
              'committer': { 'name': gitCommitterName, 'email': gitCommitterEmail},
              'sha': req.json()['sha'] }

  req = requests.delete( gitContentUrl,
                      auth = (gitUser, gitPass),
                      json = payload )

  if req.status_code == 200:
    response = jsonify ( {'status': req.status_code, 'error': "file is successfully deleted"} )
    return response

  logging.warning("status: " + str(req.status_code))
  logging.warning(json.dumps(req.text, indent=2))
  response = jsonify ( {'status': req.status_code, 'error': "could not delete file"} )
  response.status_code = req.status_code
  return response

@app.route('/<route>/files', methods=['GET'])
def listFiles(route):
  return _listFiles(route)

@app.route('/<route>/files/<filename>', methods=['GET'])
def getFile(route, filename):
  return _getFile(route, filename)

@app.route('/<route>/files/<filename>', methods=['POST'])
def createFile(route, filename):

  if not request.json:
    logging.warning('json input missing')
    response = jsonify ( {'error': 'must have json in the input'} )
    response.status_code = 400
    return response
  
  logging.warning(request.get_json(silent=True))
  return _createFile(route, filename, request.get_json(silent=True))

@app.route('/<route>/files/<filename>', methods=['PUT'])
def updateFile(route, filename):
    if not request.json:
      logging.warning('json input missing')
      response = jsonify ( {'error': 'must have json in the input'} )
      response.status_code = 400
      return response
  
    logging.warning(request.get_json(silent=True))
    return _updateFile(route, filename, request.get_json(silent=True))
 
@app.route('/<route>/files/<filename>', methods=['DELETE'])
def deleteFile(route, filename):
  return _deleteFile(route, filename)
  
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
