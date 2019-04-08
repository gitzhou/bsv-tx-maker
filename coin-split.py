import configparser
import binascii
import hashlib
import base58
import bitsv
from btclib import bip32
from btclib import bip39
from bip32utils import BIP32Key

configuration = configparser.ConfigParser()
configuration.read("app.conf")
config = configuration['coin-split']


# x_private_key String --> private_key String
def private_key_from_xprv(x_private_key):
    private_key = BIP32Key.fromExtendedKey(x_private_key)
    return binascii.b2a_hex(private_key.PrivateKey())


# private_key String --> WIF String
def wif_from_private_key(private_key, compressed=True):
    # Step 1: get the private key in extended format, this is hexadecimal upper or lower case.
    private_key_static = private_key
    # Step 2: adding 80 in the front for select de MAINNET channel bitcoin address
    extended_key = "80" + private_key_static
    if compressed:
        extended_key += "01"
    # Step 3: first process SHA-256
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    # Step 4: second process SHA-256
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # Step 5-6: add checksum info to end of extended key
    final_key = extended_key + second_sha256[:8]
    # Step 7: finally the Wallet Import Format (WIF) is generated in the format base 58 encode of final_key
    return base58.b58encode(binascii.unhexlify(final_key))


# x_private_key String --> wif String
def wif_from_xprv(x_private_key):
    private_key = private_key_from_xprv(x_private_key)
    return wif_from_private_key(private_key.decode('ascii'))


with open('send.address', 'r', encoding='utf-8') as file:
    addresses = file.readlines()
print("Found {} addresses, will split coin into {} parts first".format(len(addresses), len(addresses)))

split_addresses_count = len(addresses)

mnemonic = config['mnemonic']
master_x_private_key = bip39.mprv_from_mnemonic(mnemonic=mnemonic, passphrase='', xversion=bip32.PRV[0])
derivation_path = "m/44'/0'/0'"
satoshi = int(config['satoshi'])
fee = 296
wif_list = []
outputs = []
print('Derive address from mnemonic, save the corresponding WIF to file split.wif')
print('The mnemonic is: ' + mnemonic)
print("The derivation path is: " + derivation_path)
for i in range(0, split_addresses_count):
    xprv = bip32.derive(master_x_private_key, derivation_path + "/0/" + str(i))
    wif = wif_from_xprv(xprv.decode('ascii'))
    xpub = bip32.xpub_from_xprv(xprv)
    address = bip32.address_from_xpub(xpub).decode('ascii')
    outputs.append((address, satoshi + fee, 'satoshi'))
    wif_list.append(wif)

with open('split.wif', 'w', encoding='utf-8') as file:
    for line in wif_list:
        file.writelines(line + '\n')

money = bitsv.Key(config['wif'].strip(' '))
print("Load balance from your WIF, got {} satoshi".format(money.get_balance()))

split_tx = money.send(outputs=outputs)

with open('split.tx.hash', 'w', encoding='utf-8') as file:
    file.writelines(split_tx + '\n')

print("Split coin into {} parts, transaction hash is {}, saved to file split.tx.hash".format(len(outputs), split_tx))
print('Coin split finished')
print('Please wait for at least 1 confirmation of the split transaction, then run tx-maker.py')
