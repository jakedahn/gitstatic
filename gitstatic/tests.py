import os
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

    # @mock_s3
    # def test_create_job(self):
    #     self._stub_s3_bucket()
    #     data = {'input_scene': 'bar'}

    #     rv = self.app.post('/v0/programs/foo/jobs',
    #                        data=data,
    #                        headers={'accept': 'application/json'})
    #     assert rv.status_code == 200
    #     foos = api.find_jobs('foo')
    #     assert len(foos) == 1
    #     assert foos[0].input_scene == 'bar'

if __name__ == '__main__':
    unittest.main()
