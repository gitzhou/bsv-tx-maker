# bsv-tx-maker

Enjoy and use at your own risk.

Make sure you know what you are doing. It's running on Bitcoin SV MainNet.

This toolkit has 3 parts.

- Address crawler
  - Fetch valid BSV addresses from Memo SV profile, these addresses are `send-to` addresses
  - Save results to file `send.address`, this file is the input of `coin-split.py` and `tx-maker.py`
  - You can setup your own `send.address` file as you like, one address per line
- Coin split tool, if you have 10 send-to addresses, wanna create 10 transactions to these addresses
  - This tool derive 10 split addresses from mnemonic specified by you first
  - Then split coin, which load by your WIF, into 10 split addresses, each split address receive `842` satoshi
  - Save the coin split transaction hash to file `split.tx.hash`, the WIF of split addresses to file `split.wif`, these 2 files are the input of `tx-maker.py`
- Transaction maker, create and send transaction(send `546` satoshi at least to avoid dust payment policy)
  - One split address as input, one send-to address as output, fee is `296` satoshi
  - You should split coin first, wait for the coin split transaction meet at least 1 confirmation, then run `tx-maker.py` to avoid the unconfirmed transaction chain exceeds the 25 limitation

## How to use

Install the requirements first.

```bash
$ pip3 install -r requirements.txt
```

## Generate address

Change `app.conf` first.

```
[address-crawler]
page_start = 1
page_count = 4
```

Run `address-crawler.py` will give you valid BSV addresses from [memo sv profile](https://memo.sv/profiles/most-actions). Crawler will get address from page `page_start`, totally search `page_count` pages.

If you set `page_start = 1` and `page_count = 4`, you will get `100` addresses(`25` address per page).

```
$ python3 address-crawler.py
```

Addresses will save to file `send.address` under current folder, one address per line.

You can setup this file as you want if you have already got a BSV address list.

## Split coin

```
[coin-split]
satoshi = 546
wif = your_own_private_key_here                        # <== change me!
mnemonic = your_own_mnemonic_here_separated_by_space   # <== change me!
path = m/44'/0'/0'
```

According to the count of send-to addresses, coin split tool will derive a same count split address from mnemonic specific by you, use path `m/44'/0'/0'` by default. The derivation path of first split address is `m/44'/0'/0'/0/0`.

Then split coin, which load by your WIF, into these split addresses.

One transaction with 1 input and 1 output will cost fee `296` satoshi. Since a transaction need to send at least `546` satoshi to avoid dust payment policy, so each split address will receive `842` satoshi.

You can use [Mnemonic Code Converter](https://iancoleman.io/bip39/) to generate a mnemonic of 12 English words or use any 12-words **valid BIP-39 mnemonic** as you like.

No worries, these split addresses are only used temporarily. After sending transactions, the balance of these split addresses will be 0, nothing left.

```
$ python3 coin-split.py
```

The WIF of these coin split addresses will save to file `split.wif`, and coin split transaction hash will save to file `split.tx.hash`, these 2 files are the input of `tx-maker.py`.

**NOTICE: You need to wait for the coin split transaction meet at least 1 confirmation, to avoid the unconfirmed transaction chain exceeds the 25 limitation.**

## Generate transactions

Wait for at least 1 confirmation of the coin split transaction, then run `tx-maker.py`.

```
$ python3 tx-maker.py
```

It will create and send a transactions for each address in file `send.address`.

Transactions hash will save to file `[timestamp].tx` under current folder.

## Conclusion

- If you already have a BSV address list, put them in `send.address`. Or setup configuration file then run `address-crawler.py`
- Put you own WIF and mnemonic in configuration file, run `coin-split.py` to split coin
- Wait for the coin split transaction meet at least 1 confirmation, run `tx-maker.py` to create and send transactions 

**Under my personal test, it's OK when count of address is not more than 1000.**

**Don't change the OP_RETURN message, it will affect the transaction fee which will cause un-spendable UTXO**

Send transactions to `1000` address will cost about `0.009` BSV, FYI.

# Transactions made by this tool

- [Count statistics](http://bit.ly/2U6B0Y9)
- [Transaction list](http://bit.ly/2U3s716)

# Donation

Appreciated and THANK YOU :smile:

You can donate **Bitcoin**, **Bitcoin Cash** or **Bitcoin SV** to `13L81fdKqdif6AEFAfBymXdyB3hDvBvdp9` to buy me a cup of coffee :coffee:

![Imgur](https://i.imgur.com/oowYIk6.png)

# License

MIT
