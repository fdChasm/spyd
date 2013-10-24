class FormattedSauerbratenMessageSplitter(object):
    def __init__(self, max_length):
        self._max_length = max_length

        self._saved_color = "\f7"
        self._last_color = "\f7"

    def split(self, message):
        chunks = [bytearray(self._last_color)]
        chunk = chunks[-1]

        ix = 0
        while ix < len(message):
            if message[ix] == '\f':
                color = message[ix:ix + 2]
                ix += 2
                if color == '\fr':
                    color = self._saved_color
                elif color == '\fs':
                    self._saved_color = self._last_color
                    continue

                self._last_color = color

                if len(chunk) + len(color) > self._max_length:
                    chunks.append(bytearray(color))
                    chunk = chunks[-1]
                else:
                    chunk.extend(color)

            else:

                if len(chunk) + 1 > self._max_length or self._should_split_early(message, len(chunk), ix):
                    chunks.append(bytearray(self._last_color))
                    chunk = chunks[-1]

                if len(chunk) == 2 and message[ix] == ' ':
                    ix += 1
                    continue

                chunk.append(message[ix])

                ix += 1

        return map(bytearray.decode, chunks)

    def _should_split_early(self, message, chunklen, ix):
        seek_range = min(self._max_length - chunklen, 10, len(message) - ix)

        if message[ix] == ' ' and seek_range < 10:
            for i in xrange(1, seek_range):
                if message[ix + i] == ' ':
                    return False
            return True

        return False