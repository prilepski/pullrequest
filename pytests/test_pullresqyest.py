import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
from pullrequest import pullrequest

class TestPullRequest(object):
    def test_pullrequest_creation(self):
        pr = pullrequest.PullRequest(1)

        assert pr is not None