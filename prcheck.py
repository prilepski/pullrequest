class CheckStates:
    _ERROR = "error"
    _FAILURE = "failure"
    _PENDING = "pending"
    _SUCCESS = "success"
    _UNDEFINED = "undefined"

class PRCheck:
 
    def __init__(self, state = "", description = "", targetURL = "", context = "", serializedState = {}):
        self.initPRCheck(state, description, targetURL, context, serializedState)
        

    def initPRCheck(self, state, description, targetURL, context, serializedState = {}):
        if state is None:
            self.state = CheckStates._UNDEFINED
        elif state not in [CheckStates._ERROR, 
            CheckStates._FAILURE, 
            CheckStates._PENDING, 
            CheckStates._SUCCESS]:
            self.state = CheckStates._UNDEFINED
        else:
            self.state = state

        if description is None:
            self.description = ""
        else:
            self.description = description
        
        if targetURL is None:
            self.targetURL = ""
        else:
            self.targetURL = targetURL
        
        if context is None:
            self.context = ""
        else:
            self.context  = context

        if serializedState is None:
            self.serializedState = {}
        else:
            self.serializedState = serializedState
        
        self.statusID = 0 # Status ID from Github. Will be set when check is already stored to / loaded from Github