import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
import prcheck

class TestPRCheck(object):
    def test_prcheck_creation(self):
        # Check default initialization
        pr = prcheck.PRCheck()
        assert pr.state == prcheck.CheckStates._UNDEFINED
        assert pr.context == ""
        assert pr.description == ""
        assert pr.targetURL == ""
        assert len(pr.serializedState) == 0

        # check parameterized initialization
        state = prcheck.CheckStates._SUCCESS
        description = "some description"
        targetURL = "http://"
        context = "context"
        serializedState = {"param1": "value1", "param2": "value2"}

        pr = prcheck.PRCheck(state, description, targetURL, context, serializedState)
        assert pr.state == state
        assert pr.context == context
        assert pr.description == description
        assert pr.targetURL == targetURL
        assert len(pr.serializedState) == len(serializedState)

        # forcing all params to be None
        state = None
        description = None
        targetURL = None
        context = None
        serializedState = None

        pr = prcheck.PRCheck(state, description, targetURL, context, serializedState)
        assert pr.state == prcheck.CheckStates._UNDEFINED
        assert pr.context == ""
        assert pr.description == ""
        assert pr.targetURL == ""
        assert len(pr.serializedState) == 0

