import prcheck
import json
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PullRequest:
    _PULLS_URL = "/pulls/{}"
    def __init__(self, restAPI, user, pwd, prID):
        if restAPI is None:
            self.restAPI = ""
        else:
            self.restAPI = restAPI
        self.restAPI = self.restAPI.rstrip("//")

        if prID is None:
            self.prID = 0
        else:
            self.prID = prID #Pull request ID
        
        self.user = user
        self.pwd = pwd
        self.state = "" # Pull Request State. TODO: initialize & provide a class for states
        self.title = "" # Pull REquest title. TODO: initialize
        self.body = "" # Pull Request body. TODO: initialize
        self.baseBranch = "" # PR's target / destination branch
        self.sourceBranch= "" # PR's source branch
        self.author = "" # PR origiator
        self.isMeargiable = False # Indication if PR is mergeable
        self.mergeSHA = "" # PR's SHA
        self.checks = [] # PR status checks. Array of PRCheck

    def GetPullInfo(self):
        """
        Requests and returns json object for a given PR ID.
        Requires PullRequest object to be properly initialized with PR ID and URL to repo's REST API
            :param self: 
        """   
        if self.restAPI == "" or self.prID == 0:
            return {}
        
        response = requests.get(self.restAPI + self._PULLS_URL.format(self.prID), auth=(self.user, self.pwd), verify=False)
        if not response.ok:
            return {}
        else:
            return response.json()

    def LoadPRfromGitHub(self):
        if self.prID == 0:
            return False
        
        return True

