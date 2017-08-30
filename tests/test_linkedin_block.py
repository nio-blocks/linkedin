from nio.testing.block_test_case import NIOBlockTestCase

from ..linkedin_block import LinkedIn


class TestFeedlyStreams(NIOBlockTestCase):

    def test_process_signals(self):
        blk = LinkedIn()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
