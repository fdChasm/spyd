from cube2common.colors import color_wrappers, colors
from spyd.utils.wrapping_string_formatter import WrappingStringFormatter


smf = WrappingStringFormatter()

def clientnum_wrapper(cn):
    return color_wrappers.magenta("({})".format(cn))

def room_title_wrapper(title):
    return "{blue}{title}{white}".format(title=title, **colors)

def action_wrapper(action):
    return color_wrappers.orange("#{}".format(action))

smf.register_wrapper('name',        color_wrappers.green)
smf.register_wrapper('cn',          clientnum_wrapper)
smf.register_wrapper('pn',          clientnum_wrapper)
smf.register_wrapper('domain',      color_wrappers.magenta)
smf.register_wrapper('auth',        color_wrappers.magenta)
smf.register_wrapper('action',      action_wrapper)
smf.register_wrapper('room',        color_wrappers.blue)
smf.register_wrapper('room_title',  room_title_wrapper)
smf.register_wrapper('info',        color_wrappers.yellow)
smf.register_wrapper('error',       color_wrappers.red)
smf.register_wrapper('notice',      color_wrappers.red)
smf.register_wrapper('value',       color_wrappers.grey)
smf.register_wrapper('map',         color_wrappers.grey)
smf.register_wrapper('mode',        color_wrappers.grey)

def wrapper_function(prefix_wrapper, prefix):
    prefix_fmt = ''.join(["{", prefix_wrapper,"#prefix}: {msg_fmt}"])
    def function(msg_fmt, *args, **kwargs):
        msg_fmt = smf.format(prefix_fmt, prefix=prefix, msg_fmt=msg_fmt)
        return smf.vformat(msg_fmt, args, kwargs)
    return function
    
info   = wrapper_function('info',   'Info')
notice = wrapper_function('notice', 'Notice')
error  = wrapper_function('error',  'Error')
denied = wrapper_function('error',  'Denied')
