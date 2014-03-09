import unittest
from spyd.utils.formatted_sauerbraten_message_splitter import FormattedSauerbratenMessageSplitter

max_length = 12

class TestFormattedSauerbratenMessageSplitter(unittest.TestCase):
    def assertChunksOk(self, max_length, chunks, expected=None):
        for chunk in chunks:
            self.assertLessEqual(len(chunk), max_length)
        if expected is not None:
            self.assertEqual(expected, chunks)

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.fsms = FormattedSauerbratenMessageSplitter(max_length=max_length)

    def test_remove_color_saves_restores_restore_with_no_save(self):
        message = bytearray(b'\fr')

        result = self.fsms.remove_color_saves_restores(message)

        self.assertEqual(bytearray(b'\f7'), result)

    def test_remove_color_saves_restores_save_restore(self):
        message = bytearray(b'\f1Hi\fs \f2there\fr yo')

        result = self.fsms.remove_color_saves_restores(message)

        self.assertEqual(bytearray(b'\f1Hi \f2there\f1 yo'), result)

    def test_remove_color_saves_restores_deletes_malformated_format_controls(self):
        message = bytearray(b'te\fxt')

        result = self.fsms.remove_color_saves_restores(message)

        self.assertEqual(bytearray(b'text'), result)

    def test_remove_redundant_coloring_adjacent_color_format_controls(self):
        message = bytearray(b'text \f3\f4color')

        result = self.fsms.remove_redundant_coloring(message)

        self.assertEqual(bytearray(b'text \f4color'), result)

    def test_remove_redundant_coloring_useless_format_controls(self):
        message = bytearray(b'\f3text \f3color')

        result = self.fsms.remove_redundant_coloring(message)

        self.assertEqual(bytearray(b'\f3text color'), result)

    def test_split_short_message_no_formatting(self):
        fsms = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = bytearray(b"Hello world")

        chunks = fsms.split(message)

        self.assertChunksOk(max_length=max_length, chunks=chunks, expected=[u'Hello', u'world'])


    def test_split_continued_coloring(self):
        fsms = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = bytearray(b"\f3Hello world")

        chunks = fsms.split(message)

        self.assertChunksOk(max_length=max_length, chunks=chunks, expected=[b'\f3Hello', b'\f3world'])
