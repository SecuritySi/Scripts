#!/usr/bin/env python

import requests
import blockcypher
import sys
from pathlib import Path
from collections import Counter
import argparse
import time

def current_btc_price():

    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    resp = requests.get(url)
    return resp.json()

def wallet_check(addr):

    values = {}

    '''
    Alternative URLs to try is stuff breaks
    #https://blockexplorer.com/api/addr/1GXazHVQUdJEtpe62UFozFibPa8ToDoUn3/balance
    #https://blockexplorer.com/api/addr/1GXazHVQUdJEtpe62UFozFibPa8ToDoUn3/totalReceived
    '''
    url = "https://blockchain.info/address/{}?format=json".format(addr)
    resp = requests.get(url).json()

    values['balance'] ='{:.10f}'.format(blockcypher.from_satoshis(resp['final_balance'], 'btc'))
    values['total'] ='{:.10f}'.format(blockcypher.from_satoshis(resp['total_received'], 'btc'))

    return values


def checkout(output):

    p = Path(output)
    if p.is_file():
        return
    else:
        with open(output, 'w+') as f:
            f.write("BTC_Addr,Balance_BTC,Balance_USD,Total_BTC,Total_USD" + "\n")
        return


def getsession(todo):

    completed = []

    p = Path('session.state')
    if p.is_file():
        with open('session.state') as f:
            lines = f.read().splitlines()
        for line in lines:
            dict_obj = eval(line)
            if 'completed' in dict_obj:
                completed.append(dict_obj['completed'])
        print("Addresses completed in last session: {}".format(len(completed)))
        l1 = Counter(todo)
        l2 = Counter(completed)
        diff = list((l1 - l2).elements())

        return diff
    else:

        return todo



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="Line seperated Bitcoin address file",
                        required=True)
    parser.add_argument('--session', help="Resume previous session",
                        default=True)
    parser.add_argument('--output', help="Output CSV for lookup results -- Default 'Results.csv'",
                        default='Results.csv')


    args = parser.parse_args()
    output = args.output
    filename = args.filename

    with open(filename) as f:
        lines = f.read().splitlines()

    lines = set(lines)
    session = True

    if session:
        todo = getsession(lines)

    checkout(output)


    print("Processing: {} addresses".format(len(todo)))

    try:
        with open(output, 'a+') as f, open('session.state', 'a+') as s:
            for line in todo:


                try:
                    values = wallet_check(line)

                    market_price = current_btc_price()

                    rate = market_price['bpi']['USD']['rate'].replace(",", "")

                    balance_usd = "${}".format(round(float(values['balance']) * float(rate), 2))
                    total_usd = "${}".format(round(float(values['total']) * float(rate), 2))
                    f.write(line.strip()+","+values['balance']+","+balance_usd+","+values['total']+","+total_usd+"\n")
                    print("BTC_Addr: {},BTC_Balance: {}, USD Value: {}, BTC_Total: {}, USD Value: {}\n".format(line.strip(),values['balance'], balance_usd, values['total'], total_usd))

                    state = {"completed":line,'timestamp': time.strftime("%Y%m%d-%H%M%S")}

                    s.write(str(state)+"\n")

                except Exception as e:
                    state = {"failed": line, 'timestamp': time.strftime("%Y%m%d-%H%M%S")}
                    s.write(str(state)+"\n")
                    print(e)
                    pass

    except KeyboardInterrupt:
        print("[CTRL+C detected]")
        sys.exit(0)

if __name__ == '__main__':
    main()