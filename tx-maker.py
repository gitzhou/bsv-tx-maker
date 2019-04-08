import bitsv
import time
import requests
import configparser

configuration = configparser.ConfigParser()
configuration.read("app.conf")
config = configuration['coin-split']

message = 'Send via Bitcoin SV Transaction Maker http://bit.ly/2U15I4w'


def tx_confirmed(tx_hash):
    try:
        json = requests.get("https://api.blockchair.com/bitcoin-sv/dashboards/transaction/" + tx_hash).json()
        return json['data'][tx_hash]['transaction']['block_id'] != -1
    except:
        return False


with open('split.tx.hash', 'r', encoding='utf-8') as file:
    split_tx_hash = file.readline().strip(' ').strip('\n')

print('Split transaction detected, ' + split_tx_hash)

if not tx_confirmed(split_tx_hash):
    print('Please wait for at least 1 confirmation of the split transaction, then run tx-maker.py')
    exit(0)

with open('split.wif', 'r', encoding='utf-8') as file:
    wif_list = file.readlines()

with open('send.address', 'r', encoding='utf-8') as file:
    addresses = file.readlines()

if len(wif_list) != len(addresses):
    print('Line count in file send.address and split.wif is not match')
    exit(0)

money_list = []
for wif in wif_list:
    money_list.append(bitsv.Key(wif.strip(' ').strip('\n')))

print('Everything is fine, start to create and send transactions')
print('---------------------------------------------------------')

index = 0
transactions = []
satoshi = config['satoshi']
for address in addresses:
    address = address.strip(' ').strip('\n')
    outputs = [
        (address, satoshi, 'satoshi')
    ]
    tx = money_list[index].send(outputs=outputs, message=message)
    print(address + ' ' + tx)
    index += 1
    transactions.append(tx)

with open('{}.tx'.format(time.strftime("%Y%m%d%H%M%S", time.localtime())), 'w', encoding='utf-8') as file:
    for tx in transactions:
        file.writelines(tx + '\n')
