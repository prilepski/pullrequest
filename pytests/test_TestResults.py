import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
import testresults
import requests

def Mock_RequestsPost(url, data, auth, verify):
    return requests.Response()

def Mock_JSON(self):
    data = {
        'id': str('1'),
        'number': str('123')
    }
    return data

def Mock_JSON_Negative(self):
    data = {
    }
    return data

class TestTestResults(object):

    user = 'prilepski'
    pwd = 'password'
    restAPIURL = 'https://api.github.com/repos/prilepski/pullrequest/'

    def test_BaseClass_Tests(self):
        # Test incorrect initialization
        testsEmpty = testresults.TestResults(None, None)
        # Should be no elements & no reply by the name 
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.GetTestResult('test') is None

        # Test that loading test results is initiated
        testsEmpty = testresults.TestResults('filename', None)
        # Should be no elements
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.GetTestResult('test') is None

        testsEmpty = testresults.TestResults('filename', testresults.TestSystems.JUNIT)
        # Should be no elements
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.testSystem == testresults.TestSystems.JUNIT

        testsEmpty = testresults.TestResults('filename', testresults.TestSystems.JUNIT)
        # Should be no elements
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.testSystem == testresults.TestSystems.JUNIT

    def test_JUnit_LoadTestResults(self):
        testsEmpty = testresults.JUnitTestResults('')
        # jsonShould be no elements
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.GetTestResult('something') is None
        assert testsEmpty.GetTestResults() == {}

        testsEmpty = testresults.JUnitTestResults(None)
        # Should be no elements
        assert testsEmpty.GetTestResultsNum() == 0
        assert testsEmpty.GetTestResult('something') is None
        assert testsEmpty.GetTestResults() == {}

        test8OK = testresults.JUnitTestResults('./pytests/datafiles/TestTestResults_8_success.xml')
        assert test8OK.GetTestResultsNum() == 8
        assert len(test8OK.GetSuccessfulTests()) == 8
        assert len(test8OK.GetFailedTests()) == 0

        test8Failure = testresults.JUnitTestResults('./pytests/datafiles/TestTestResults_8_failure.xml')
        assert test8Failure.GetTestResultsNum() == 8
        assert len(test8Failure.GetSuccessfulTests()) == 4
        assert len(test8Failure.GetFailedTests()) == 4
        testDictionary = test8Failure.GetTestResults()
        assert len(testDictionary) == 8

        for key, value in testDictionary.iteritems():
            assert value.name == test8Failure.GetTestResult(key).name
          
    def test_RegisterTestResults(self, monkeypatch):
        def Mock_RegisterBulkResults(self, testResults):
            return -1
#    def test_RegisterTestResults(self):

        monkeypatch.setattr(requests, 'post', Mock_RequestsPost)
        monkeypatch.setattr(requests.Response, 'json', Mock_JSON)

        test8Failure = testresults.JUnitTestResults('./pytests/datafiles/TestTestResults_8_failure.xml')
        assert test8Failure.GetTestResultsNum() == 8
        assert len(test8Failure.GetSuccessfulTests()) == 4
        assert len(test8Failure.GetFailedTests()) == 4

        assert test8Failure.RegisterTestResults(None) == -1

        baseTestSystemObj = testresults.BaseTestSystem()
        assert test8Failure.RegisterTestResults(baseTestSystemObj) == -1

        # only failed tests are to be registered
        githubTestSystemObj = testresults.GitHubTestSystem(self.restAPIURL, self.user, self.pwd)
        assert test8Failure.RegisterTestResults(githubTestSystemObj) == 4

        # No failures - no results to be registered
        test8OK = testresults.JUnitTestResults('./pytests/datafiles/TestTestResults_8_success.xml')
        assert test8OK.RegisterTestResults(githubTestSystemObj) == 0

        # test how empty test results are covered
        testEmpty = testresults.TestResults('', None)
        assert testEmpty.RegisterTestResults(baseTestSystemObj) == 0

        # test if base implementation can register tests individually if Buulk method is not implemented
        # case 1: all successfull results. They all will be registered as RegisterTestResult registeres all
        monkeypatch.setattr(testresults.GitHubTestSystem, 'RegisterBulkResults', Mock_RegisterBulkResults)
        assert test8OK.RegisterTestResults(githubTestSystemObj) == 8

        # case 2: mixure of failed and successful tests
        assert test8Failure.RegisterTestResults(githubTestSystemObj) == 8

        # Empty results
        assert testEmpty.RegisterTestResults(githubTestSystemObj) == 0

        monkeypatch.undo()

class TestBaseTestSystem(object):
     def test_RegisterBulkResults(self):
        
        # Check that base class bulk registration is not implemented
        test8Failure = testresults.JUnitTestResults('./pytests/datafiles/TestTestResults_8_failure.xml')
        testSystem = testresults.BaseTestSystem()
        assert testSystem.RegisterBulkResults(test8Failure.GetTestResults()) == -1

        # check that registering indivudual item is not implemented
        for item in test8Failure.GetTestResults().itervalues():
            assert testSystem.RegisterTestResult(item) == -1

class TestGitHubTestSystem(object):
    user = 'prilepski'
    pwd = 'password'
    restAPIURL = 'https://api.github.com/repos/prilepski/pullrequest/'

    def test_RegisterTestResult(self, monkeypatch):
        testElement = testresults.TestElement(
            'test.class', 
            'testName', 
            'test body',
            1,
            2,
            1
        )
        testElement.priority = testElement.Priority.Blocker
        testElement.severity = testElement.Severity.High
        testElement.component = 'Test Component'
        testElement.sub_component = 'Test Sub-Component'

        githubTestSystemObj = testresults.GitHubTestSystem(self.restAPIURL, self.user, self.pwd)
        monkeypatch.setattr(requests, 'post', Mock_RequestsPost)
        monkeypatch.setattr(requests.Response, 'json', Mock_JSON)
        assert githubTestSystemObj.RegisterTestResult(testElement) == 1

        monkeypatch.setattr(requests.Response, 'json', Mock_JSON_Negative)
        assert githubTestSystemObj.RegisterTestResult(testElement) == 0

        monkeypatch.undo()