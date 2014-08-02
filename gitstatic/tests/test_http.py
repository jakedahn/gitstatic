import json
import http
import unittest

class TestJobsHTTP(unittest.TestCase):

    def setUp(self):
        self.app = http.app.test_client()

    def tearDown(self):
        pass

    def _valid_request_body(self):
        return 'foo'

    def test_root(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_build_post_git_url(self):
        data = {'git_url': 'git@github.com:foo/bar.git'}
        rv = self.app.post('/build', data=data,
                                     headers={'accept': 'application/json'})
        assert rv.status_code == 202
        res_json = json.loads(rv.data)
        assert res_json['msg'] == 'git url received'

if __name__ == '__main__':
    unittest.main()
