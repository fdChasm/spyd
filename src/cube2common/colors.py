colors = {
    'green'  : '\f0',
	'blue'   : '\f1',
	'yellow' : '\f2',
	'red'    : '\f3',
	'grey'   : '\f4',
	'magenta': '\f5',
	'orange' : '\f6',
	'white'  : '\f7',
}

save = '\fs'
restore = '\fr'

class color_wrappers(object):
    """@DynamicAttrs"""
    pass

def get_color_wrapper(color_fmt):
    return staticmethod(lambda v: "{}{}{}{}".format(save, color_fmt, v, restore))

for color_name, color_fmt in colors.iteritems():
    setattr(color_wrappers, color_name, get_color_wrapper(color_fmt))
