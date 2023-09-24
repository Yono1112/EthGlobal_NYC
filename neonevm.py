from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider("https://devnet.neonevm.org"))

contract_address = "CONTRACT_ADDRESS"

contract_abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newMessage",
                "type": "string"
            }
        ],
        "name": "updateMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "message",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

private_key = "MYPRIVATEKEY"

acct = w3.eth.account.from_key(private_key)

construct_txn = contract.functions.updateMessage("New Message").build_transaction({
  "from": acct.address,
  "nonce": w3.eth.get_transaction_count(acct.address),
  "gas": 5000000,
  "gasPrice": w3.to_wei("300", "gwei")
})

signed = acct.sign_transaction(construct_txn)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# エラーを避けるためにログの存在を確認する
if receipt["logs"]:
    print(receipt["logs"][0]["data"])
else:
    print("No logs found.")
