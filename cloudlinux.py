#!/usr/bin/env python
# coding: utf-8
# vim: tabstop=2 noexpandtab
"""
    Author: Danilo F. Chilene
    Email:  bicofino at gmail dot com
"""

import requests
import json
import exceptions


class EndpointsMixin(object):

    def status(self, params=None):
        """ https://cln.cloudlinux.com/api/status.plain
        Return system information about several Cloudlinux services
        """
        endpoint = 'status.json'
        return self.request(endpoint, params=params)

    def availability(self, ip, **params):
        """URL example: https://cln.cloudlinux.com/api/ipl/availability.json?ip=1.1.1.1&token=AUTH_TOKEN
        Will return information about what kind of license types are available for registration and what
        types are already used by current account
        """
        params['ip'] = ip
        endpoint = 'ipl/availability.json'
        return self.request(endpoint, params=params)

    def check(self, ip, **params):
        """URL: https://cln.cloudlinux.com/api/ipl/check.json?ip=1.1.1.1&token=AUTH_TOKEN
        Check if IP license is registered by any customer.
        """
        params['ip'] = ip
        endpoint = 'kcare/check.json'
        return self.request(endpoint, params=params)

    def register_server(self, key, **params):
        """URL: https://cln.cloudlinux.com/api/kcare/register_server.json?key=WsTs821nSAtiastD
        Will register KC server by KernalCare Key
        """
        params['key'] = key
        endpoint = 'kcare/register_server.json'
        return self.request(endpoint, params=params)

    def register(self, ip, license_type, **params):
        """URL: https://cln.cloudlinux.com/api/kcare/register_server.json?key=WsTs821nSAtiastD
        Will register KC server by KernalCare Key
        """
        params['ip'] = ip
        params['type'] = license_type
        endpoint = 'ipl/register.json'
        return self.request(endpoint, params=params)

    def remove(self, ip, license_type, **params):
        """URL: https://cln.cloudlinux.com/ipl/remove.json?ip=1.1.1.1&type=16&token=AUTH_TOKEN
        Will remove IP based license from authorized user licenses.
        """
        params['ip'] = ip
        params['type'] = license_type
        endpoint = 'ipl/remove.json'
        return self.request(endpoint, params=params)

    def unregister_server(self, server_id, **params):
        """URL: https://cln.cloudlinux.com/api/kcare/unregister_server.json?server_id=a8621dsasdf923hs
        Will remove server registration for KC key
        """
        params['server_id'] = server_id
        endpoint = 'kcare/unregister_server.json'
        return self.request(endpoint, params=params)

    def create_key(self, limit, note, **params):
        """URL: https://cln.cloudlinux.com/api/kcare/key/create.json?token=AUTH_TOKEN&limit=2&note=Key+description
        Will generate new KC key for authorized user
        """
        params['limit'] = limit
        params['note'] = note
        endpoint = 'kcare/key/create.json'
        return self.request(endpoint, params=params)

    def delete_key(self, key, **params):
        """URL: https://cln.cloudlinux.com/api/kcare/key/delete.json?token=AUTH_TOKEN&key=WsTs821nSAtiastD
        Will delete KC key owned by authorized user
        """
        params['key'] = key
        endpoint = 'kcare/key/delete.json'
        return self.request(endpoint, params=params)

    def list(self, params=None):
        """URL: https://cln.cloudlinux.com/api/ipl/list.json?token=AUTH_TOKEN
        Return all IP licenses owned by authorized user.
        """
        endpoint = 'ipl/list.json'
        return self.request(endpoint, params=params)

    def server(self, ip, **params):
        """URL: https://cln.cloudlinux.com/api/ipl/server.json?token=AUTH_TOKEN&ip=1.1.1.1
        Return all IP licenses owned by authorized user filtered by ip
        """
        params['ip'] = ip
        endpoint = 'ipl/server.json'
        return self.request(endpoint, params=params)


class API(EndpointsMixin, object):

    def __init__(self, access_token=None, headers=None):
        """Instantiates an instance of CloudLinux API wrapper
        :param access_token: (optional) Provide a valid access token
        """

        self.api_url = 'https://cln.cloudlinux.com/api'

        self.access_token = access_token
        self.client = requests.Session()

    def request(self, endpoint, method='GET', params=None):
        """Returns dict of response from CloudLinux API
        :param endpoint: (required) (e.g. kcare/register_server.json)
        :type endpoint: string
        :param method: (optional) Method of accessing data, GET or POST.
         (default GET)
        :type method: string
        :param params: (optional) Dict of parameters(if any) accepted by
        CloudLinux API endpoint you are trying to access (default None)
        :type params: dict or None"""
        url = '{0}/{1}'.format(self.api_url, endpoint, self.access_token)
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)

        request_args = {}
        if method == 'get':
            request_args['params'] = params
            request_args['params']['token'] = self.access_token
        else:
            request_args['data'] = params

        try:
            response = func(url, **request_args)
            print response.url
            content = response.content.decode('utf-8')
        except requests.RequestException as e:
            print (str(e))
            content = dict(error=str(e))
        print content
        content = json.loads(content)

        if response.status_code >= 400:
            raise exceptions.CloudLinuxError(content)
        return content
