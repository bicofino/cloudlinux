#!/usr/bin/env python
# coding: utf-8
# vim: tabstop=2 noexpandtab
"""
    Author: Danilo F. Chilene
    Email:  bicofino at gmail dot com
"""


class CloudLinuxError(Exception):
    """ Generic error class"""
    def __init__(self, error_response):
        self.error_response = error_response
        msg = "CloudLinux API returned error code {0} ({1})".format(
                error_response['code'], error_response['message']
                )
        super(CloudLinuxError, self).__init__(msg)
