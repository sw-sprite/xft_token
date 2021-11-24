import xrpl
import pickle
import json



with open('wallet/wallet1.pkl', 'rb') as inp1:
    cold_wallet = pickle.load(inp1)
with open('wallet/wallet2.pkl', 'rb') as inp2:
    hot_wallet = pickle.load(inp2)

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

# Configure issuer (cold address) settings -------------------------------------
cold_settings_tx = xrpl.models.transactions.AccountSet(
    account = cold_wallet.classic_address,
    # transfer rate is 1000000000 - 2000000000, fee to charge, 0 means no fee
    transfer_rate= 0,  
    tick_size = 5,
    domain = bytes.hex("example.com".encode("ASCII")),
    set_flag = xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
)

cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=cold_settings_tx,
    wallet=cold_wallet,
    client=client,
)

print("Sending cold address AccountSet transaction...")
response = xrpl.transaction.send_reliable_submission(cst_prepared, client)
print(json.dumps(response.result, indent=4))

# Configure hot address settings -----------------------------------------------
hot_settings_tx = xrpl.models.transactions.AccountSet(
    account=hot_wallet.classic_address,
    set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
)
hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=hot_settings_tx,
    wallet=hot_wallet,
    client=client,
)
print("Sending hot address AccountSet transaction...")
response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
print(json.dumps(response.result, indent=4))


# set currency detail
currency_code = "XFT"
trust_set_tx = xrpl.models.transactions.TrustSet(
    account=hot_wallet.classic_address,
    limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
        currency=currency_code,
        issuer=cold_wallet.classic_address,
        value="10000000000",  # Large limit, arbitrarily chosen
    )
)
ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=trust_set_tx,
    wallet=hot_wallet,
    client=client,
)
print("Creating trust line from hot address to issuer...")
response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
print(json.dumps(response.result, indent=4))


# Send token -------------------------------------------------------------------
issue_quantity = "4000000"
send_token_tx = xrpl.models.transactions.Payment(
    account=cold_wallet.classic_address,
    destination=hot_wallet.classic_address,
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
    f"Sending {issue_quantity} {currency_code} to {hot_wallet.classic_address}...")
response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
print(json.dumps(response.result, indent=4))

# Check balances ---------------------------------------------------------------
print("Getting hot address balances...")
response = client.request(xrpl.models.requests.AccountLines(
    account=hot_wallet.classic_address,
    ledger_index="validated",
))
print(json.dumps(response.result, indent=4))

print("Getting cold address balances...")
response = client.request(xrpl.models.requests.GatewayBalances(
    account=cold_wallet.classic_address,
    ledger_index="validated",
    hotwallet=[hot_wallet.classic_address]
))
print(json.dumps(response.result, indent=4))
