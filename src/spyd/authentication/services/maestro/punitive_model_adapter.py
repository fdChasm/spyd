from spyd.punitive_effects.punitive_effect_info import EffectInfo, PermaExpiryInfo


class PunitiveModelAdapter(object):
    def __init__(self, puntive_model):
        self._punitive_model = puntive_model
    
    def add_ban(self, effect_desc):
        effect_info = EffectInfo(PermaExpiryInfo())
        self._punitive_model.add_effect('ban', effect_desc, effect_info)
    
    def clear_bans(self):
        self._punitive_model.clear_effects('ban')
