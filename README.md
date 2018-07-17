# Overview
This Pull Request Handling project attempts cover engineering ide of Continous Delivery (CD):
- triggering builds and tests for Pull Requests (PR)
- automatically merging PRs into target branch in case of successful tests
- reporting test results and failures into supported Test Management ad DEfect Tracking systems
- reporting code coverage results.

The project is incomplete and slowly evolving (as time permits). Current State section provides information on what is done and what will be coming.
[] add link to section above

# Current State
- Wrapper classes to work with GitHub's Pull Requests
- Wrapper classes to deal with test results and publish results into supported test systems

[] Create Jenkins pipeline skeleton
[] Create actual test pipeline that will build, test and report test results

# Usage
[] TBD

# Conributions & Cutomization
## How to Contribute
[] This repo was meant to be open for contribution, but exact procedure is TBD. If you wish to contribute, contact repo ownder or simply copy it for your own needs.

## How to Build & Test
[] This needs to be modified once enough integration is implemented and PullRequest repo uses its own code for PR testing

At this time the following to be used:
### Running Tests
```
py.test pytests
```

### Generating Code Coverage
```
py.test --cov=. --cov-report=annotate --cov-report=html
```

### Storing Test Results using JUnit Format
```
py.test --junitxml=./junit.xml
```

### Combinig All of the Above Together
```
py.test --cov=. --cov-report=annotate --cov-report=html --junitxml=./junit.xml
```

## Customization & Extension Possibilities
[] TBD

# Class Diagram
[] TBD. Add graphical diagram

## PRCheck
Wraps and implements operations with Pull Request status checks. They are used by Pull Request handler to describe, report and persist status of all checks associated with Pull Requests. 

### CheckStates
Defines valid PRCheck states.

## PullRequest
Implements wrapper to work with GutHub's Pull Requests

## BaseTestSystem
Base class implementing interactions with test systems.
BaseTestystem class is to be inherited and extended to implement interation with a given test system. See GitHubTestSystem as an example.

## GitHubTestSystem
Implements interactions with "issues" at GitHub. Extends BaseTestSystem with GitHub specifics.


## TestSystems
Is an ENUM of known Test Systems. GitHub is the only one supported for now. The rest are in there as examples.

## TestElement
Describes and implementes properties and functionality of a single test result (result of a particular single test execution).

## TestResults
Base class implementing properties and functionality of a test result list. A list that consist of instances of TestElement objects.

## JUnitTestResults
Class that inherits and extends basic TestResults implementation to interact with JUnit test result format.   
