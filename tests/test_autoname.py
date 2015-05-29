# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from swift.common.swob import Request

from autoname import middleware


class FakeApp(object):
    def __init__(self):
        self.headers = []

    def __call__(self, env, start_response):
        start_response('201 CREATED', self.headers)

        return []


def start_response(*args):
    pass


class TestAutoName(unittest.TestCase):
    def test_put(self):
        app = middleware.AutoNameMiddleware(FakeApp(), {})

        req = Request.blank('/auto/AUTH_test/container/',
                            environ={'REQUEST_METHOD': 'PUT',
                                     })
        res = req.get_response(app)
        self.assertEqual(res.status_int, 201)
        self.assertTrue('X-Object-Meta-Public-Autoname' in res.headers)


if __name__ == '__main__':
    unittest.main()
