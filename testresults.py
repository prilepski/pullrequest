class TestElement:
    def __init__(self, name, iter, duration, result):
        self.name = name
        self.iter = iter
        self.duration = duration
        self.result = result

class PyTestCycloneElement(TestElement):
    def __init__(self, name, iter, duration, result):
        self.name = name
        self.iter = iter
        self.duration = duration
        if 'Pass' == result:
            self.result = 1
        else:
            self.result = 0

class TestResults:
    def __init__(self, strInputArray):
        self.testResults = {}
        if strInputArray:
            self.LoadTestResults(strInputArray)

    def LoadTestResults(self, strInputArray):
        self.testResults.clear()
        return 0
    
    def GetTestResult(self, strTestName):
        if not strTestName:
            return None
        else:
            return self.testResults.get(strTestName, None)

class PyTestCycloneTestResults(TestResults):
    
    def LoadTestResults(self, strInputArray):
        # Loading will always clean whatever was in the list
        self.testResults.clear()

        if not strInputArray:
            return 0

        bStartParsing = False
        for line in strInputArray:
            if not bStartParsing:
                if any(x.upper() in line.upper() for x in ['Module', 'Test Name', 'Iter', 'Duration', 'Result']):
                    # found last line just before test results
                    bStartParsing = True
            else:
                if '|' not in line:
                    # all test result lines contain '|' 
                    pass
                else:
                    lineArray = line.split('|')
                    self.testResults[lineArray[1].strip() + "." + lineArray[2].strip()] = PyTestCycloneElement(
                        lineArray[1].strip() + "." + lineArray[2].strip(), 
                        lineArray[3].strip(), 
                        lineArray[4].strip().rstrip('s'), 
                        lineArray[5].strip())
        return len(self.testResults)



