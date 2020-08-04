class JobPositionCandidate():

    def __init__(self, idclient=0, idjobposition=0, idcandidate=0, date_registered, 
                 user_register, user_registered_byself=True):
        self.idclient = idclient
        self.idjobposition = idjobposition
        self.idcandidate = idcandidate
        self.date_registered = date_registered
        self.user_register = user_register
        self.user_registered_byself = user_registered_byself
