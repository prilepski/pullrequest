import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
from pullrequest import pullrequest
import json
import requests
import prcheck

def Mock_ResponseJSON(param):
    return json.load(open("./pytests/datafiles/test_GetPullInfo_positive.json"))

class TestPullRequest(object):
    user = "prilepski"
    pwd = "dmitri0404"


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
        
        # TODO: use mocks to avoid calling github here
        CheckPR("https://api.github.com/repos/prilepski", 1, self.user, self.pwd) # Positive Test
        CheckPR(None, 1, self.user, self.pwd) # Negative test: no URL
        CheckPR("https://api.github.com/repos/prilepski", None, self.user, self.pwd) # Negative test: no PR ID
        CheckPR("https://api.github.com/repos/prilepski", 1, None, self.pwd) # Negative test: no user
        CheckPR("https://api.github.com/repos/prilepski", 1, self.user, None) # Negative test: no pwd
        CheckPR(None, None, None, None) # Negative test: all missing

    def test_GetPullInfo(self, monkeypatch):
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
        # TODO: test for negative cases when LoadPRfromGitHub is extended
        monkeypatch.setattr(pullrequest.PullRequest, "GetPullInfo", Mock_ResponseJSON)
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", self.user, self.pwd, prID)
        assert pr.LoadPRfromGitHub() == True

    def test_add_del_Check(self):
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", self.user, self.pwd, prID)

        assert len(pr.checks) == 0 # should be no checks
        context = "test check"
        state = prcheck.CheckStates._FAILURE
        description = "some description"
        target_url = "http://some.url"

        # test for adding a check
        pr.addCheck(context, state, description, target_url)
        assert not pr.checks[context] is None
        assert pr.checks[context].state == state
        assert pr.checks[context].description == description
        assert pr.checks[context].targetURL == target_url
        assert len(pr.checks) == 1 # should be 1 check exactly

        # add the same check again. Should just update existing one
        description = "new description"
        pr.addCheck(context, state, description, target_url)
        assert len(pr.checks) == 1 # should still be 1 item
        assert pr.checks[context].description == description # check if descriptiongot updated

        # add with empty context. Nothing should be added
        context = ""
        assert pr.addCheck(context, state, description, target_url) is None

        # delete element
        assert pr.delCheck("test check") == True
        #delete it agains
        assert pr.delCheck("test check") == False
        # delete with empty key
        assert pr.delCheck("") == False
        
        
        
    def test_SaveChecks(self, monkeypatch):
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", self.user, self.pwd, prID)
        
        check = prcheck.PRCheck(prcheck.CheckStates._PENDING, "test check", "http://emc.com", "Test Check", [])

        pr.checks["test check"] = check
        assert pr.checks["test check"].statusID == 0 # expecting statusID to be 0
        assert len(pr.SaveChecks()) == 0 # expect empty response (no errors)
        assert pr.checks["test check"].statusID <> 0 # and now it should be set into something non zero

