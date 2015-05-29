# Copyright (c) 2015 Christian Schwede <cschwede@redhat.com>
#
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

import uuid

from swift.common.utils import split_path


class AutoNameMiddleware(object):

    def __init__(self, app, conf, *args, **kwargs):
        self.app = app

    def __call__(self, env, start_response):
        try:
            (version, account, container, objname) = split_path(
                env['PATH_INFO'], 1, 4, True)
        except ValueError:
            return self.app(env, start_response)

        autoname = str(uuid.uuid4())

        def _start_response(status, headers, exc_info=None):
            headers.append(('X-Object-Meta-Public-Autoname', autoname))
            return start_response(status, headers, exc_info)

        if (container and not objname and
                env['PATH_INFO'][-1] == '/' and
                env['REQUEST_METHOD'] == 'PUT'):
            env['PATH_INFO'] = "/%s/%s/%s/%s" % (
                version, account, container, autoname)
            return self.app(env, _start_response)
        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def autoname_filter(app):
        return AutoNameMiddleware(app, conf)
    return autoname_filter
