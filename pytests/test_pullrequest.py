import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
from pullrequest import pullrequest
import json
import requests

class TestPullRequest(object):
    user = "user"
    pwd = "pwd"
    def test_pullrequest_creation(self):
        pr = pullrequest.PullRequest("http://", 1, self.user, self.pwd)
        assert pr is not None

    def test_GetPullInfo(self, monkeypatch):
        def Mock_ResponseJSON(param):
            return json.load(open("./test_GetPullInfo_positive.json"))
        def Mock_RequestsGet(url, auth, verify):
            return requests.Response()

        # wrong URL
        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/wrong/", prID, self.user, self.pwd)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # PR ID = 0
        prID = 0
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/wrong/", prID, self.user, self.pwd)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # empty URL
        prID = 1
        pr = pullrequest.PullRequest("", prID, self.user, self.pwd)
        json_response = pr.GetPullInfo()
        assert json_response.get("number", "") == ""

        # happy path test
        monkeypatch.setattr(requests.Response, 'json', Mock_ResponseJSON)
        monkeypatch.setattr(requests, 'get', Mock_RequestsGet)

        prID = 1
        pr = pullrequest.PullRequest("https://api.github.com/repos/prilepski/pullrequest/", prID, self.user, self.pwd)
        json_response = pr.GetPullInfo()
        assert json_response["number"] == prID
