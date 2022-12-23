from ds_protocol import extract_json, encode_json, DataTuple
import unittest, time

class extract_json_test(unittest.TestCase):
    def test_extract_json_dm(self):
        json_obj = extract_json('{"response": {"type": "ok", "message": "Direct message sent"}}')
        real = DataTuple('O', '', 'Direct message sent')

        self.assertEqual(json_obj, real)
    
    def test_extract_json_all(self):
        json_obj = extract_json('{"response": {"type": "ok", "messages": \
        [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}')
        real = DataTuple('O', '', [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"}, {"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}])
        
        self.assertEqual(json_obj, real)

    def test_extract_json_failed(self):
        json_obj = extract_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript" "timestamp":"1603167689.3928561"}]}}')
        real = DataTuple('E', '', 'Json cannot be decoded.')

        self.assertEqual(json_obj, real)

class encode_json_test(unittest.TestCase):
    def test_encode_json_join(self):
        json_msg = encode_json('join', user='testperson', extra='abc123')
        real = '{"join": {"username": "testperson", "password": "abc123", "token": ""}}'

        self.assertEqual(json_msg, real)
    
    def test_encode_json_dm(self):
        json_msg = encode_json('directmessage', 'Hello World!', "user_token", "ohhimark", "send")
        real = '{"token": "user_token", "directmessage": {"entry": "Hello World!", "recipient": "ohhimark", "timestamp": "'+ str(time.time()) +'"}}'

        self.assertEqual(json_msg, real)
    
    def test_encode_json_all(self):
        json_msg = encode_json('directmessage', token='user_token', extra='new')
        real = '{"token": "user_token", "directmessage": "new"}'
        
        self.assertEqual(json_msg, real)
    
    def test_encode_json_new(self):
        json_msg = encode_json('directmessage', token='user_token', extra='all')
        real = '{"token": "user_token", "directmessage": "all"}'
        
        self.assertEqual(json_msg, real)
    
if __name__ == '__main__':
    unittest.main()
    