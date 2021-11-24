import xrpl
import pickle
# from xrpl.wallet import generate_faucet_wallet
# from xrpl.clients import JsonRpcClient

with open('wallet/wallet1.pkl', 'rb') as inp:
    wallet = pickle.load(inp)

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = xrpl.clients.JsonRpcClient(JSON_RPC_URL)
print(xrpl.account.does_account_exist(
    wallet.classic_address, client))
