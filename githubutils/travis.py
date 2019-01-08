import json
import urllib
from githubutils.ghauth import GitHubAuthentication

class Travis(GitHubAuthentication):
    
    root = "http://api.travis-ci.org/"

    def __init__(self, token=None):
        super(Travis, self).__init__(None, token)

    def _getNextURL(self, resp):
        jsonResp = json.loads(resp.text)
        if (not '@pagination' in jsonResp):
            return None
        if (jsonResp['@pagination'] is None):
            return None
        if (jsonResp['@pagination']['next'] is None):
            return None
        return self.root + jsonResp['@pagination']['next']['href']

    def _processResp(self, url, resp):
        if (resp is None):
            return None
        jsonResp = json.loads(resp.text)
        if ('build' in jsonResp):
            return jsonResp['build']
        return jsonResp

    def getBuilds(self, repoSlug):
        encodedSlug = urllib.parse.quote(repoSlug,safe='')
        return self.genericApiCall(self.root, "/repo/" + encodedSlug + "/builds", "limit", 
                headers={'Travis-API-Version': '3'})

    def getBuild(self, buildId):
        return self.__makeCall("/build/" + str(buildId))

    def __makeCall(self, endpoint, params={}, headers={}):
        headers['Travis-API-Version'] = '3'
        return self.genericApiCall(self.root, endpoint, "limit", headers=headers)

    def makeCall(self, endpoint):
        return self.__makeCall(endpoint)