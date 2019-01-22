#!/usr/bin/env python3

from shodan import Shodan
import netaddr
import time

'''
Quick and dirty script to pull out historical results from Shodan API.
'''

API_KEY = 'KEY'

api = Shodan(API_KEY)


netblock = 'NETBLOCK'

net = netaddr.IPNetwork(netblock)

for IP in net:

    try:
        time.sleep(1)
        fileout = open('shodan_result.stxt', 'a')
        res = api.host(str(IP), history=True)
        host_json = {}
        port_list = []
        for banner in sorted(
                res["data"],
                key=lambda k: (k["port"], k["timestamp"])
        ):

            if "timestamp" in banner and banner["timestamp"]:
                date = banner["timestamp"][:10]
            else:
                date = ""
            port_list.append(str(banner["port"]) + ":" + str(date))

        host_json = {'ipaddr':str(IP), 'ports':port_list}
        fileout.write(str(host_json) + "\n")
        fileout.close()
    except Exception as e:
        print('[!] Error: {}'.format(e))
