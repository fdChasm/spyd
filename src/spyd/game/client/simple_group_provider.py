class SimpleGroupProvider(object):
    def __init__(self, *group_names):
        self.group_names = group_names

    def get_group_names(self):
        return self.group_names