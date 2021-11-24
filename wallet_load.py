from xrpl.models.requests.account_info import AccountInfo
import pickle
import json
import xrpl
from xrpl.wallet import generate_faucet_wallet
from xrpl.asyncio.account import get_balance
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

with open('wallet/wallet3.pkl', 'rb') as inp:
    wallet = pickle.load(inp)

test_account = wallet.classic_address
acct_info = AccountInfo(
    account=test_account,
    ledger_index="validated",
    strict=True,
)
response = client.request(acct_info)
result = response.result
print(json.dumps(result, indent=4, sort_keys=True))
# Check balances ---------------------------------------------------------------
print("Getting hot address balances...")
response = client.request(xrpl.models.requests.AccountLines(
    account=wallet.classic_address,
    ledger_index="validated",
))
print(json.dumps(response.result, indent=4))


# print("Getting cold address balances...")
# response = client.request(xrpl.models.requests.GatewayBalances(
#     account=cold_wallet.classic_address,
#     ledger_index="validated",
#     hotwallet=[hot_wallet.classic_address]
# ))
# print(response)
