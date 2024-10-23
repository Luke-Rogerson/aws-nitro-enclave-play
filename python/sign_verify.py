from web3 import Web3
from eth_account.messages import encode_defunct

PRIVATE_KEY = '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


w3 = Web3()

msg = 'Hello world'

message = encode_defunct(text=msg)
signed_message = w3.eth.account.sign_message(message, private_key=PRIVATE_KEY)
print(signed_message.signature.hex())

encoded_msg = encode_defunct(text=msg)
recovered_address = w3.eth.account.recover_message(encoded_msg, signature=signed_message.signature.hex())
print('recovered_address:', recovered_address)
account = w3.eth.account.from_key(PRIVATE_KEY)
print('signer_address:', account.address)
print(recovered_address == account.address)