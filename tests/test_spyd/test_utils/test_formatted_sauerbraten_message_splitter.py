import unittest
from spyd.utils.formatted_sauerbraten_message_splitter import FormattedSauerbratenMessageSplitter

max_length = 12

class TestFormattedSauerbratenMessageSplitter(unittest.TestCase):
    def assertChunksOk(self, max_length, chunks):
        for chunk in chunks:
            self.assertEqual(chunk[0], '\f')
            self.assertLessEqual(len(chunk), max_length)

    def test_short_message_no_formatting(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = "Hello world"

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=max_length, chunks=chunks)

    def test_overlength_message_no_formatting(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = "Hello world, how are you"

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=max_length, chunks=chunks)

    def test_overlength_message_with_formatting_in_first_message(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = "Hello \f2world, Goodbye"

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=max_length, chunks=chunks)

    def test_overlength_message_with_save_restore_in_first_message(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=max_length)

        message = "Hel\fslo \f2wor\frld, Goodbye"

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=max_length, chunks=chunks)

    def test_commands_message_save_reset_colors_correctly(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=512)

        message = 'Commands: \x0cs\x0c6commands\x0cr | \x0cs\x0c6follow\x0cr | \x0cs\x0c6timeleft\x0cr | \x0cs\x0c6room_create\x0cr | \x0cs\x0c6room\x0cr | \x0cs\x0c6rooms\x0cr'

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=512, chunks=chunks)

    def test_commands_with_short_word_at_end(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=512)

        message = 'test small chunk with short word at end.'

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=512, chunks=chunks)

    def test_save_reset_working_correctly(self):
        formatted_sauer_message_splitter = FormattedSauerbratenMessageSplitter(max_length=512)

        message = '\x0cs\x0c2Info\x0cr: \x0cs\x0c0\x0cs\x0c0[FD]Chasm\x0cr\x0cr claimed auth as \x0cs\x0c5chasm\x0cr@\x0cs\x0c5localhost\x0cr'

        chunks = formatted_sauer_message_splitter.split(message)

        # print chunks

        self.assertChunksOk(max_length=512, chunks=chunks)
