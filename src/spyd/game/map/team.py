class Team(object):
    def __init__(self, team_id, name):
        self.id = team_id
        self.name = name
        
        self.score = 0
        self.oflags = 0
        self.frags = 0
        self.size = 0
