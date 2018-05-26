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
        self.checks = {} # PR status checks. Dictionary of PRChecks
        self.prJSON = {}

        self.LoadPRfromGitHub() # Load data from Github

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
        self.prJSON = self.GetPullInfo()
        if len(self.prJSON) == 0:
            return False
        
        return True

    def SaveChecks(self):
        """
        creates/updates statuses for Pull Request based on array of checks
        Args:
            <None>
        Returns:
            dictionary: json response in case of error and empty dictionry if success
        """   
        for check in self.checks.items():
            data = {
                'state': check.state,
                'target_url': check.targetURL,
                'context': check.context,
                'description': json.dumps(check.serializedState)
            }
            
            resp = requests.post(self.getStatusesURL(), data=json.dumps(data), auth=(self.user, self.pwd), verify=False)
            if not resp.ok:
                return resp # Return information on failed items
            else:
                # update check with Status ID
                check.statusID = resp.json().get("id", 0)
                return {} # returning empty disctionary on success

    def getStatusesURL(self):
        """
        returns URL to Github Status REST API call
        Args:
            <None>
        Returns:
            string: statuses GtiHub API url or empty string in case of errors.
        """   
        # TODO: check out how to use interally
        return self.prJSON.get("statuses_url", "")

    def addCheck(self, context, status, description, target_url):
        # TODO: creare a class to cover possible context values instead of just plain string
        """
        returns URL to Github Status REST API call
        Args:
            string: context for status check
            string: state of the check. MAy take values from CheckStates class
            string: description to be used for the check
            straing: target URL To be passed to a check 
        Returns:
            PRCheck: returns check object or None (in case of issues)
        """   
        if len(context) == 0:
            return None
        newCheck = prcheck.PRCheck(status, description, target_url, context)

        self.checks[context] = newCheck

    def delCheck(self, context):
        if self.checks.pop("context", 0) != 0:
            return True
        else:
            return False