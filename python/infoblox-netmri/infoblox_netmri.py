# Copyright 2015 Infoblox Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import requests


class InfobloxNetMRI(object):
    def __init__(self, options):
        """Initialize a new InfobloxNetMRI object

        Args:
            options (dict): Target options dictionary
        """

        self.sslverify = True
        if 'sslverify' in options:
            self.sslverify = options['sslverify']

        reqd_opts = ['url', 'username', 'password']
        default_opts = {'http_pool_connections': 5,
                        'http_pool_maxsize': 10,
                        'max_retries': 5}
        for opt in reqd_opts + default_opts.keys():
            setattr(self, opt, options.get(opt) or default_opts.get(opt))

        for opt in reqd_opts:
            if not getattr(self, opt):
                raise ValueError("Option %s is missing" % opt)

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=self.max_retries,
            pool_connections=self.http_pool_connections,
            pool_maxsize=self.http_pool_maxsize)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.auth = (self.username, self.password)
        self.session.verify = self.sslverify

    def _controller_name(self, objtype):
        # would be better to use inflect.pluralize here, but would add
        # a dependency
        if objtype.endswith('y'):
            return objtype[:-1] + 'ies'

        if objtype[-1] in 'sx' or objtype[-2:] in ['sh', 'ch']:
            return objtype + 'es'

        if objtype.endswith('an'):
            return objtype[:-2] + 'en'

        return objtype + 's'

    def _controller_url(self, objtype):
        return "%s/%s" % (self.url, self._controller_name(objtype))

    def _method_url(self, method_name):
        return "%s/%s" % (self.url, method_name)

    def api_request(self, method_name, params):
        """Execute an arbitrary method.

        Args:
            method_name (str): include the controller name: 'devices/search'
            params (dict): the method parameters
        Returns:
            A dict with the response
        Raises:
            requests.exceptions.HTTPError
        """

        headers = {'Content-type': 'application/json'}

        url = self._method_url(method_name)
        data = json.dumps(params)

        r = self.session.post(url,
                              data=data,
                              verify=self.sslverify,
                              headers=headers)

        r.raise_for_status()

        return json.loads(r.content)

    def show(self, objtype, objid):
        """Query for a specific resource by ID

        Args:
            objtype (str): object type, e.g. 'device', 'interface'
            objid (int): object ID (DeviceID, etc.)
        Returns:
            A dict with that object
        Raises:
            requests.exceptions.HTTPError
        """
        headers = {'Content-type': 'application/json'}

        url = "%s/%d" % (self._controller_url(objtype), objid)

        r = self.session.get(url,
                             verify=self.sslverify,
                             headers=headers)


        r.raise_for_status()

        return json.loads(r.content)[objtype]

    def delete(self, objtype, objid):
        """Destroy a specific resource by ID

        Args:
            objtype  (str): object type, e.g. 'script'
            objid (int): object ID
        Returns:
            A dict with the response
        Raises:
            requests.exceptions.HTTPError
        """

        headers = {'Content-type': 'application/json'}

        url = "%s/%d" % (self._controller_url(objtype), objid)

        r = self.session.delete(url,
                             verify=self.sslverify,
                             headers=headers)

        r.raise_for_status()

        return json.loads(r.content)
