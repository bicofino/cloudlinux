#!/usr/bin/env python
# coding: utf-8
# vim: tabstop=2 noexpandtab
"""
    Author: Danilo F. Chilene
    Email:  bicofino at gmail dot com
"""

import argparse
import time
import hashlib
from cloudlinuxapi import cloudlinux

auth_user = 'YourUser'
secret = 'xxx'


def generate_token():
    ts = int(time.time())
    hash_object = hashlib.sha1(b'{0}{1}'.format(secret, ts))
    hex_dig = hash_object.hexdigest()
    final_token = '{0}|{1}|{2}'.format(auth_user, ts, hex_dig)
    return final_token


kernelcare = cloudlinux.API(access_token=generate_token())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--action',
        help='check, register, remove, servers',
        type=str)
    parser.add_argument('--ip', help='IP to register', type=str)
    parser.add_argument('--type', type=str, help='License type [1,2 or 16]')
    args = parser.parse_args()
    if args.action == 'check':
        kernelcare.check(ip=args.ip)
    elif args.action == 'register':
        kernelcare.register(ip=args.ip, license_type=args.type)
    elif args.action == 'remove':
        kernelcare.remove(ip=args.ip, license_type=args.type)
    elif args.action == 'server':
        kernelcare.server(ip=args.ip)
    elif args.action == 'list':
        servers = kernelcare.list()
        total_servers = len(servers['data'])
        total_registered = []
        total_unregistered = []
        for server in servers['data']:
            if server['registered'] is True:
                total_registered.append(server)
            else:
                total_unregistered.append(server)
        print 'Total servers: ' + str(total_servers)
        print len(total_registered)
        print len(total_unregistered)
    elif args.action == 'list-unregistered':
        servers = kernelcare.list()
        print '----'
        for server in servers['data']:
            if server['registered'] is False:
                print server
    else:
        parser.print_usage()
