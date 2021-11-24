# Prepare payment
import xrpl as xrpl
from xrpl.transaction import send_reliable_submission
from xrpl.clients import JsonRpcClient
import pickle
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.wallet import generate_faucet_wallet

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

with open('wallet/wallet1.pkl', 'rb') as inp:
    wallet = pickle.load(inp)

my_tx_payment = Payment(
    account="rKzaY7pr8bAgiUQcSVqkrcU7UWW2qsFmY1",
    amount=xrp_to_drops(22),
    destination="rLNd2sqL5k6daJPb9Ka8cW282ssTT8Rzoe",
)

# Sign the transaction
my_tx_payment_signed = safe_sign_and_autofill_transaction(
    my_tx_payment, wallet, client)

# Submit and send the transaction
tx_response = send_reliable_submission(my_tx_payment_signed, client)

print(tx_response)