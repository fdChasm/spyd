class Flag(object):
    id = 0
    team = None
    version = 0
    spawn = -1
    invisible = 0
    owner = None
    dropper = None
    drop_count = 0
    drop_location = None
    drop_time = None
    
    def __init__(self, game_clock, fid, spawn_loc, team):
        self.game_clock = game_clock
        self.id = fid
        self.team = team
        self.return_scheduled_callback_wrapper = None

    def reset(self):
        self.owner = None
        self.dropper = None
        self.drop_count = 0
        self.drop_location = None
        
        if self.return_scheduled_callback_wrapper is not None:
            self.return_scheduled_callback_wrapper.cancel()
        self.return_scheduled_callback_wrapper = None
    
    @property
    def dropped(self):
        return self.owner is None and self.drop_location is not None
    
    def drop(self, location, return_timeout):
        if self.owner is not self.dropper:
            self.drop_count = 0
        self.drop_count += 1
        self.dropper = self.owner
        self.owner = None
        self.drop_location = location

        self.return_scheduled_callback_wrapper = self.game_clock.schedule_callback(return_timeout)
