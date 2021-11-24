# Look up info about your account
import json
import pickle
import xrpl
from xrpl.models.requests.account_info import AccountInfo

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = xrpl.clients.JsonRpcClient(JSON_RPC_URL)

with open('wallet/wallet3.pkl', 'rb') as inp:
    wallet = pickle.load(inp)
    
acct_info = AccountInfo(
    account=wallet.classic_address,
    ledger_index="validated",
    strict=True,
)
response = client.request(acct_info)
result = response.result
print("response.status: ", response.status)
print(json.dumps(response.result, indent=4, sort_keys=True))
