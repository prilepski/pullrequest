import os, sys
sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
import testresults

class TestTestResuls(object):

    def test_load_test_results(self):

        testsEmpty = testresults.PyTestCycloneTestResults('')
        # Should be no elements
        assert len(testsEmpty.testResults) == 0

        testsEmpty = testresults.PyTestCycloneTestResults(None)
        # Should be no elements
        assert len(testsEmpty.testResults) == 0

        with open('./pytests/datafiles/test_TestResults_output.txt') as f:
            lines = f.readlines()
        
        # Should be no elements
        testsEmpty.LoadTestResults(None)
        assert len(testsEmpty.testResults) == 0
        # Should be exactly 592 elements
        assert testsEmpty.LoadTestResults(lines) == 592

        tests592 = testresults.PyTestCycloneTestResults(lines)
        # Should be exactly 592 elements
        assert len(tests592.testResults) == 592

        # this test must be FAILING
        assert tests592.GetTestResult('raid_full_stack_degraded_reboot.py.test_raid_degraded_log_reboot').result == 0

        assert tests592.GetTestResult('') == None
