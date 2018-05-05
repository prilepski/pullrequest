import prcheck
import json
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PullRequest:
    _PULLS_URL = "/pulls/{}"
    def __init__(self, restAPIURL, user, pwd, prID):
        if restAPIURL is None:
            self.restAPIURL = ""
        else:
            self.restAPIURL = restAPIURL
        self.restAPIURL = self.restAPIURL.rstrip("//")

        if prID is None:
            self.prID = 0
        else:
            self.prID = prID #Pull request ID

        if user is None:
            self.user = ""
        else:        
            self.user = user
        
        if pwd is None:
            self.pwd = ""
        else:
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
        Args:
            <None>
        Returns:
            json / dictionary: with Pull Request Information JSON object from Github
        """   
        if self.restAPIURL == "" or self.prID == 0:
            return {}
        
        response = requests.get(self.restAPIURL + self._PULLS_URL.format(self.prID), auth=(self.user, self.pwd), verify=False)
        if not response.ok:
            return {}
        else:
            return response.json()

    def LoadPRfromGitHub(self):
        """
        Loads Pull Request Information from GitHub
        and populates current PullRequest Object with information
        Args:
            <None>
        Returns:
            bool: True if loaded successfuly. False otherwise
        """   
        prJSON = self.GetPullInfo()
        if len(prJSON) == 0:
            return False
        return True

