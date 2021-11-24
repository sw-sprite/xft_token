import xrpl
import pickle
import json

with open('wallet/wallet1.pkl', 'rb') as inp1:
    cold_wallet = pickle.load(inp1)
with open('wallet/wallet3.pkl', 'rb') as inp1:
    receive_wallet = pickle.load(inp1)
with open('wallet/wallet2.pkl', 'rb') as inp2:
    send_wallet = pickle.load(inp2)

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

currency_code = "XFT"
issue_quantity = "42096"

# # setup trust line
# trust_set_tx = xrpl.models.transactions.TrustSet(
#     account=receive_wallet.classic_address,
#     limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
#         currency=currency_code,
#         issuer=cold_wallet.classic_address,
#         value="10000000000",  # Large limit, arbitrarily chosen
#     )
# )
# ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
#     transaction=trust_set_tx,
#     wallet=receive_wallet,
#     client=client,
# )
# print("Creating trust line from receive address to issuer...")
# response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
# print(response)

# send some tokens
send_token_tx = xrpl.models.transactions.Payment(
    account=cold_wallet.classic_address,
    destination=receive_wallet.classic_address,
    amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
        currency=currency_code,
        issuer=cold_wallet.classic_address,
        value=issue_quantity
    )
)
pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=send_token_tx,
    wallet=cold_wallet,
    client=client,
)
print(
    f"Sending {issue_quantity} {currency_code} to {receive_wallet.classic_address}...")
response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
print(json.dumps(response.result, indent=4))
