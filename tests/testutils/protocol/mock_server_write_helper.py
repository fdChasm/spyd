from contextlib import contextmanager
from mock import patch
import re

import sauerpyd.protocol.server_write_helper
import testutils.protocol.server_write_helper
from utils.exit_stack import ExitStack


put_message_method_pattern = re.compile("^put_")
put_message_method_names = filter(put_message_method_pattern.match, dir(sauerpyd.protocol.server_write_helper))

@contextmanager
def mock_server_write_helper():
    "Causes the server_write_helper module to write (N_MESSAGE, {key: data}) messages rather than binary data."
    with ExitStack() as stack:
        context = patch('cube2common.cube_data_stream.CubeDataStream', new=list)
        stack.enter_context(context)
        
        for put_message_method_name in put_message_method_names:
            if hasattr(testutils.protocol.server_write_helper, put_message_method_name):
                put_message_method = getattr(testutils.protocol.server_write_helper, put_message_method_name)
                context = patch('sauerpyd.protocol.server_write_helper.{}'.format(put_message_method_name), new=put_message_method)
                stack.enter_context(context)
        yield stack
