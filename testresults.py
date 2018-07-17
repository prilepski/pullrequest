from enum import Enum
from xml.etree import ElementTree
import json
import requests
from enum import Enum

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TestElement(object):
    class Severity(Enum):
        Undefined = -1
        Blocker = 0
        High = 1
        Medium = 2
        Low = 3

    class Priority(Enum):
        Undefined = -1
        Blocker = 0
        High = 1
        Medium = 2
        Low = 3

    def __init__(self, classname, name, body, iter, duration, result):
        self.classname = classname
        self.name = name
        self.body = body
        self.iter = iter
        self.duration = duration
        self.result = result
        self.severity = TestElement.Severity.Undefined
        self.priority = TestElement.Priority.Undefined
        self.component = ''
        self.sub_component = ''

    def isSuccess(self):
        """
        Returns True if test passed successfully
           :param self: 
        """   
        if self.result == 1:
            return True
        else:
            return False

class TestSystems(Enum):
    RALLY = "Rally"
    JUNIT = "JUnit"
    GITHUB = "GitHub"
    UNKNOWN = "Unknown"

class BaseTestSystem(object):
    """
    Base class implementing generic operations with Test Management System.
    """ 
    def RegisterBulkResults(self, testResults):
        """
        Register Test Results in one of the supported test management systems.
        To be overloaded by specific test system implementations
        Returns -1 if not supported, or number of registered test results
            :param self:
            :param testResults: dictionary of TestElement results to be registered
        """ 
        # implement iterations through test results in self.TestResults
        return -1

    def RegisterTestResult(self, testElement):
        """
        Register individual test result in one of the supported test management systems.
        To be overloaded by specific test system implementations
        Returns -1 if not supported, or number of registered test results (0 or 1 in this case)
            :param self:
            :param testElement: instance of TestElement results to be registered
        """ 
        return -1

class GitHubTestSystem(BaseTestSystem):
    _titleDefectTemplate = '{} failed'
    _titleTestResultsTemplate = '{} passed'
    _labelBug = 'bug'
    _labelTestResults = 'Test Results'

    def __init__(self, restAPIURL, user, pwd):
        self._user = user
        self._pwd = pwd
        if restAPIURL is None:
            self.restAPIURL = ''
        else:
            self._restAPIURL = restAPIURL
            self._restAPIURL = self._restAPIURL.rstrip('//')

            self._issuesURL = '/issues'

        return
    
    def RegisterBulkResults(self, testResults):
        """
        GitHubTestSystem::RegisterBulkResults
        Registers failed / error test results into github as issues
        Returns number of successfully registered test results
            :param self:
            :param testResults: Dictionary of TestElement items with test results
        """ 
        registeredResults = 0
        for item in testResults.itervalues():
            if not item.isSuccess():
                if self.RegisterTestResult(item) > 0:
                    registeredResults += 1
                
        return registeredResults

    def RegisterTestResult(self, testItem):
        """
        GitHubTestSystem::RegisterTestResult
        Registers provided test result into github as an issue
        Returns number of successfully registered test results (0 or 1 in this case)
            :param self:
            :param testResults: instance of TestElement
        """
        defectLabel = ''
        defectTitle = ''
        if testItem.isSuccess():
            defectLabel = self._labelTestResults
            defectTitle = self._titleTestResultsTemplate.format(testItem.classname + '.' + testItem.name)
        else:
            defectLabel = self._labelBug
            defectTitle = self._titleDefectTemplate.format(testItem.classname + '.' + testItem.name)

        
        labels = []
        if len(defectLabel) > 0:
            labels.append(defectLabel)
        if len(str(testItem.priority)) > 0:            
            labels.append(str(testItem.priority))
        if len(str(testItem.severity)) > 0:
            labels.append(str(testItem.severity))
        if len(testItem.component) > 0:
            labels.append(testItem.component)
        if len(testItem.sub_component):
            labels.append(testItem.sub_component)
        data = {
            'title': str(defectTitle),
            'body': testItem.body,
            'labels': labels
        }

        resp = requests.post(self._restAPIURL + self._issuesURL, data=json.dumps(data), auth=(self._user, self._pwd), verify=False)
        if not resp.ok:
            return -1 # there is an error with request
        else:
            # check if we received issue ID and number
            if resp.json().get('id', False) and resp.json().get('number', False):
                return 1 # one test result just got registered and github issue has been created
            else:
                return 0 # something went wrong: we tried, but issue has not been created or we received unexpected response



class TestResults(object):
    """
    Base class implementing operations with test reulsts
    Test result could be of supported types defined in TestSystems
    """ 
    def __init__(self, strFile, testSystem):
        """
        Init Test Results of defined type with content from specified file
            :param self: 
            :param strFile: file with test results content 
            :param testSystem: one of the supported test systems from TestSystems
        """ 
        self.testResults = {}
        if strFile:
            self.LoadTestResults(strFile)

        if not testSystem in TestSystems:
            self.testSystem = TestSystems.UNKNOWN
        else:
            self.testSystem = testSystem
    
    def LoadTestResults(self, strFile):
        """
        TestResults::LoadTestResults
        Loading test results from specified file. To be overloaded
        Returns True if successfull
            :param self:
            :param strFile: file with test results content 
        """ 
        return 0
    
    def GetTestResult(self, strTestName):
        """
        TestResults::GetTestResult
        Returns results of the speicifed test: instance of TestElement or None.
            :param self:
            :param strTestName: test name to be checked 
        """

        return self.testResults.get(strTestName, None)

    def GetTestResults(self):
        """
        TestResults::GetTestResults
        Returns dictionary with all test results.
            :param self:
            :param strTestName: test name to be checked 
        """
        return self.testResults

    def GetFailedTests(self):
        """
        TestResults::GetFailedTets
        Returns dictionary of failed tests
            :param self:
        """
        failedTests = {}
        for key, value in self.testResults.iteritems():
            if not value.isSuccess():
                failedTests[key] = value
        return failedTests

    def GetSuccessfulTests(self):
        """
        TestResults::GetFailedTets
        Returns dictionary of successful tests
            :param self:
        """
        okTests = {}
        for key, value in self.testResults.iteritems():
            if value.isSuccess():
                okTests[key] = value
        return okTests

    def GetTestResultsNum(self):
        """
        TestResults::GetTestResultsNum
        Returns number of test results. To be overloaded.
            :param self:
        """
        return len(self.testResults)

    def RegisterTestResults(self, testSystemObj):
        """
        TestResults::RegisterTestResults
        Register Test Results in one of the supported test management systems
        Returns -1 in case of error or number of registered results in case of success
            :param self: 
            :param testSystemObj: Test system object (of TestSystems class) to register results into
        """
        if testSystemObj is None:
            return -1

        bulkRegisterResult = testSystemObj.RegisterBulkResults(self.testResults)
        if -1 != bulkRegisterResult:
            return bulkRegisterResult # REturn number of registered test results

        # Bulk serialization is not supported. Register one by one
        registeredResults = 0
        for item in self.testResults.itervalues():
            testRegistration = testSystemObj.RegisterTestResult(item)
            if 0 < testRegistration:
                registeredResults += 1 # test result was registered
            elif -1 == testRegistration:
                return -1 # Unsupported single test registration method            
        
        return registeredResults
    
class JUnitTestResults(TestResults):

    _TESTCASE_TAG = 'testcase'
    _ERROR_TAG = 'error'
    _FAILURE_TAG = 'failure'
    _CLASSNAME_TAG = 'classname'
    _NAME_TAG = 'name'
    _TIME_TAG = 'time'

    def __init__(self, strFile):
        super(JUnitTestResults, self).__init__(strFile, TestSystems.JUNIT)

    def LoadTestResults(self, strFile):
        # Loading will always clean whatever was in the list
        testTree = ElementTree.parse(strFile)
        testRoot = testTree.getroot()

        self.testResults.clear()
        # Iterate through all testcase elements
        for elem in testRoot.findall(self._TESTCASE_TAG):
            testResult = 0
            if elem.find(self._ERROR_TAG) is not None:
                # This test case finished with error
                testResult = 0
            elif elem.find(self._FAILURE_TAG) is not None:
                # This test case finished with failure
                testResult = 0
            else:
                # This test case finished with success
                testResult = 1

            self.testResults[elem.get(self._CLASSNAME_TAG) + '.' + elem.get(self._NAME_TAG)] = TestElement(
                elem.get(self._CLASSNAME_TAG),
                elem.get(self._NAME_TAG),
                '', # replace with passing body
                1,
                elem.get(self._TIME_TAG),
                testResult)

        return self.GetTestResultsNum()



