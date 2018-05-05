import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
from pullrequest import pullrequest
import json
import requests

def Mock_ResponseJSON(param):
    return json.load(open("./test_GetPullInfo_positive.json"))

class TestPullRequest(object):
    user = "user"
    pwd = "pwd"


    def test_pullrequest_creation(self):
        def CheckPR(restAPIURL, prID, user, pwd):
            prObject = pullrequest.PullRequest(restAPIURL, user, pwd, prID)
            if restAPIURL is None:
                restAPIURL = ""
            if user is None:
                    user = ""
            if pwd is None:
                pwd =""
            if prID is None:
                prID = 0

            assert restAPIURL.rstrip("/") == prObject.restAPIURL
            assert prID == prObject.prID
            assert pwd == prObject.pwd
            assert user == prObject.user
        
        CheckPR("http://", 1, self.user, self.pwd) # Positive Test
        CheckPR(None, 1, self.user, self.pwd) # Negative test: no URL
        CheckPR("http://", None, self.user, self.pwd) # Negative test: no PR ID
        CheckPR("http://", 1, None, self.pwd) # Negative test: no user
        CheckPR("http://", 1, self.user, None) # Negative test: no pwd
        CheckPR(None, None, None, None) # Negative test: all missing

    def test_GetPullInfo(self, monkeypatch):
        def Mock_ResponseJSON(param):
            return json.load(open("./test_GetPullInfo_positive.json"))
        def Mock_RequestsGet(url, auth, verify):
            return requests.Response()

        # wrong URL
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/wrong/", self.user, self.pwd, prID)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # PR ID = 0
        prID = 0
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/wrong/", self.user, self.pwd, prID)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # empty URL
        prID = 1
        pr = pullrequest.PullRequest("", self.user, self.pwd, prID)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # happy path test
        monkeypatch.setattr(requests.Response, 'json', Mock_ResponseJSON)
        monkeypatch.setattr(requests, 'get', Mock_RequestsGet)

        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", self.user, self.pwd, prID)
        json_response = pr.GetPullInfo()
        assert json_response["number"] == prID

    def test_LoadPRfromGitHub(self, monkeypatch):
        monkeypatch.setattr(pullrequest.PullRequest, "GetPullInfo", Mock_ResponseJSON)
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", self.user, self.pwd, prID)
        assert pr.LoadPRfromGitHub() == True
        # TODO: test for negative cases when LoadPRfromGitHub is extended
