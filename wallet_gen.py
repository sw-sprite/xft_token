# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html
import pickle
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
test_wallet = generate_faucet_wallet(client, debug=True)

file_name = "wallet/wallet3."
with open(file_name+"txt", "w") as wallet1:
    print(f"public_key: {test_wallet.public_key}", file=wallet1)
    print(f"private_key: {test_wallet.private_key}", file=wallet1)
    print(f"seed: {test_wallet.seed}", file=wallet1)
    print(f"sequence: {test_wallet.sequence}", file=wallet1)
    print(f"classic_address: {test_wallet.classic_address}", file=wallet1)

with open(file_name+"pkl", "wb") as wallet1pk:
    pickle.dump(test_wallet, wallet1pk, pickle.HIGHEST_PROTOCOL)
print(test_wallet)

