class PullRequest:
    def __init__(self, prID):
        self.prID = prID #Pull request ID
        self.state = "" # Pull Request State. TODO: initialize & provide a class for states
        self.title = "" # Pull REquest title. TODO: initialize
        self.body = "" # Pull Request body. TODO: initialize
        self.baseBranch = "" # PR's target / destination branch
        self.sourceBranch= "" # PR's source branch
        self.author = "" # PR origiator
        self.isMeargiable = False # Indication if PR is mergeable
        self.mergeSHA = "" # PR's SHA
        self.checks = [] # PR status checks. TODO: replays with array of special classes
        
