from Profile import Profile, Post
from ds_messenger import DirectMessage, DirectMessenger
import ds_messenger as messenger
import unittest, time

class DirectMessage_Test(unittest.TestCase):
    def test_one(self):
        dm = DirectMessage('ohhimark', "Hello World!", time.time())
        temp = {"recipient": "ohhimark", "entry": "Hello World!", "timestamp": time.time()}

        self.assertEqual(dm, temp)

class DirectMessenger_Test(unittest.TestCase):
    def test_send_success(self):
        msg = DirectMessenger(messenger.dsuserver, 'personone', 'abc123')
        res = msg.send('Hello World!', 'test')

        self.assertTrue(res)
    
    def test_send_fail(self):
        msg = DirectMessenger(messenger.dsuserver, 'personone', 'abc1234')
        res = msg.send('Hello World!', 'test')

        self.assertFalse(res)

    def test_new(self):
        msg = DirectMessenger(messenger.dsuserver, 'personone', 'abc123')
        res = msg.retrieve_new()

        self.assertIsInstance(res, list)

    def test_all(self):
        msg = DirectMessenger(messenger.dsuserver, 'personone', 'abc123')
        res = msg.retrieve_all()

        self.assertIsInstance(res, list)

if __name__ == "__main__":
    unittest.main()