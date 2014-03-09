import re
import textwrap

FMT_CTRL = ord('\f')
SAVE = ord('s')
RESTORE = ord('r')
DEFAULT = ord('7')
COLORS = {ord(c) for c in '01234567'}

adjacent_color_pattern = re.compile(r'\f[0-7](\f[0-7])')
adjacent_color_replacement = r'\1'

def get_last_color(chunk):
    pos = chunk.rfind('\f')
    if pos != -1 and (pos + 1 < len(chunk)):
        return chunk[pos+1]
    return DEFAULT

class FormattedSauerbratenMessageSplitter(object):
    def __init__(self, max_length):
        self._max_length = max_length

        self.text_wrapper = textwrap.TextWrapper(width=max_length - 2, break_long_words=True, drop_whitespace=True, replace_whitespace=False)

    def split(self, message):
        if isinstance(message, bytearray):
            message = bytearray(message)
        else:
            message = bytearray(message, 'utf_8')

        message = self.remove_color_saves_restores(message)
        message = self.remove_redundant_coloring(message).decode('utf_8')
        chunks = [bytearray(chunk, 'utf_8') for chunk in self.text_wrapper.wrap(message)]
        return [chunk.decode('utf_8') for chunk in self.colorize_chunks(chunks)]

    def remove_color_saves_restores(self, message):
        """Treats the save & restore color codes as pushing to a stack.
        Resolves these codes to absolute colors."""
        assert(isinstance(message, bytearray))

        last_color = DEFAULT
        saved_colors = []

        def push_color(color):
            saved_colors.append(color)

        def pop_color():
            if len(saved_colors):
                return saved_colors.pop()
            return DEFAULT

        mlen = len(message)

        i = 0
        while i < mlen:
            if message[i] == FMT_CTRL and (i + 1) < mlen:
                if message[i + 1] == SAVE:
                    push_color(last_color)
                    del message[i:i + 2]
                    mlen -= 2
                elif message[i + 1] == RESTORE:
                    last_color = pop_color()
                    message[i + 1] = last_color
                    i += 2
                elif message[i + 1] in COLORS:
                    last_color = message[i + 1]
                    i += 2
                else:
                    del message[i]
                    mlen -= 1
            else:
                i += 1

        return message

    def remove_redundant_coloring(self, message):
        "Removes adjacent colors and duplicate successive uses of the same color."
        assert(isinstance(message, bytearray))

        last_color = DEFAULT

        mlen = len(message)

        i = 0
        while i < mlen:
            if message[i] == FMT_CTRL and (i + 1) < mlen:
                if message[i + 1] in COLORS:
                    if message[i + 1] == last_color:
                        del message[i:i + 2]
                        mlen -= 2
                    else:
                        last_color = message[i + 1]
                        i += 2
            else:
                i += 1

        return adjacent_color_pattern.sub(adjacent_color_replacement, message)

    def colorize_chunks(self, chunks):
        "Continues coloring from one chunk to the next."
        ci = 1
        while ci < len(chunks):
            previous_chunk_final_color = get_last_color(chunks[ci - 1])
            if previous_chunk_final_color != DEFAULT:
                chunks[ci][0:0] = [FMT_CTRL, previous_chunk_final_color]
            ci += 1

        return chunks
