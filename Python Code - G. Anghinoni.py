from web3 import Web3, Account
import json
import sys
import os

file = open("/sys/devices/w1_bus_master1/w1_master_slaves")
w1_slaves = file.readlines()
file.close()

print ("Sensor ID | Temperature")
print ("==============|============")

# Initial values of the parameters counter and elecSum
counter=0
elecSum=0

# Loop of 30 counts comparable to 30 days that are, in the end, summed
while(counter<30):
    for line in w1_slaves:
        counter = counter + 1
        w1_slave = line.split("\n") [0]
        file = open('/sys/bus/w1/devices/' + str(w1_slave) +'/w1_slave')
        filecontent = file.read()
        file.close()
    

        stringvalue = filecontent.split("\n")[1].split(" ")[9]
        temperature = float(stringvalue[2:]) / 1000

        print(str(w1_slave) +' | '+' %6.1f °C' % temperature)
        print("counter = ", str(counter))
        elecSum=elecSum + temperature
        print("Sum of electricity is = ",(elecSum))
        if counter==30:
            print("Deadline reached")
            break

# elecSum is turned into a integer
modified_value = int(elecSum)
print(round(modified_value))

# The Web3 provider is set to the local blockchain (using Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Deployment of the smart contract and obtaining its abi and bytecode
with open("/home/pi/Desktop/Code/artifacts/FundTransfer_compData (1).json") as f:
   contract_abi = json.load(f)["abi"]
with open("/home/pi/Desktop/Code/artifacts/FundTransfer_compData (1).json") as f:
   contract_bytecode = json.load(f)["bytecode"]["object"]

# Creation of the smart contract class by means of abi and bytecode
contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# The private key of the account that initialize the transaction is needed
private_key_sender = '0x343cb22d13e9e1f00d7680d04f067a01510c1906b435db1afd810e977fd31299'

# Set the sender address as the first account in Ganache and show its balance
sender_address = web3.eth.accounts[0]
print(f"Initial sender balance: {web3.eth.get_balance(sender_address)}")

# Get the nonce (number of transactions sent by the sender_address)
nonce = web3.eth.get_transaction_count(sender_address)

# Build the initial transaction using the constructor function of the smart contract
transaction = contract.constructor().build_transaction({
    'from': sender_address,
    'nonce': nonce,
    'value': web3.to_wei('2', 'ether'), # Amount of Ether sent from the sender_address to the contract
    'gas': 5000000,
    'gasPrice': web3.to_wei('10', 'gwei')  # Transaction cost in gwei
})

# Sign the transaction with the private key
signed_txn = web3.eth.account.sign_transaction(transaction, private_key_sender)

# Send the signed transaction to the blockchain
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Get the transaction receipt in order to obtain the address of the deployed contract
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Show the contract address and balance after its deployment
print("Contract Address:", contract_address)
print(f"Contract balance: {web3.eth.get_balance(contract_address)}")
# Show the balance of the sender_address before triggering the withdraw function
print(f"Sender balance before the withdraw function: {web3.eth.get_balance(sender_address)}")

# Set the recipient address as the second account in Ganache and show its balance
recipient_address = web3.eth.accounts[1]
print(f"Recipient balance before the transaction: {web3.eth.get_balance(recipient_address)}")
# Set the current_value parameter as the monthly sum of temperature values
current_value = modified_value

# Encode function call
tx_data = contract.encodeABI(fn_name='ConditionalTransaction', args=[recipient_address, current_value])

# Build the main transaction of the smart contract
transaction_main = {
    'to': contract_address,
    'from': sender_address,
    'nonce': web3.eth.get_transaction_count(sender_address),
    'gas': 500000,
    'gasPrice': web3.to_wei('10', 'gwei'),
    'data': tx_data,
}

signed_txn_main = web3.eth.account.sign_transaction(transaction_main, private_key_sender)

tx_hash_main = web3.eth.send_raw_transaction(signed_txn_main.rawTransaction)

tx_receipt_main = web3.eth.wait_for_transaction_receipt(tx_hash_main)

# Encode function call
tx_data_transaction = contract.encodeABI(fn_name='TransferWhenMet', args=[recipient_address])

# Build the transaction "TransferWhenMet"
transaction_ether = {
    'to': contract_address,
    'from': sender_address,
    'nonce': web3.eth.get_transaction_count(sender_address),
    'gas': 500000,
    'gasPrice': web3.to_wei('10', 'gwei'),
    'data': tx_data_transaction,
}

signed_txn_ether = web3.eth.account.sign_transaction(transaction_ether, private_key_sender)

tx_hash_ether = web3.eth.send_raw_transaction(signed_txn_ether.rawTransaction)

tx_receipt_ether = web3.eth.wait_for_transaction_receipt(tx_hash_ether)

# Encode function call 
tx_data_withdraw = contract.encodeABI(fn_name='withdrawEthereum')

# Build the withdraw transaction
withdraw_function = {
    'to': contract_address,
    'from': sender_address,
    'nonce': web3.eth.get_transaction_count(sender_address),
    'gas': 500000,
    'gasPrice': web3.to_wei('10', 'gwei'),
    'data': tx_data_withdraw,
}

signed_txn_withdraw = web3.eth.account.sign_transaction(withdraw_function, private_key_sender)

tx_hash_withdraw = web3.eth.send_raw_transaction(signed_txn_withdraw.rawTransaction)

tx_receipt_withdraw = web3.eth.wait_for_transaction_receipt(tx_hash_withdraw)

# Show the transaction hash
print("Transaction Hash:", tx_hash.hex())
# Show the final balances of the contract, sender_address and recipient_address
print(f"Final contract balance: {web3.eth.get_balance(contract_address)}")
print(f"Final sender balance: {web3.eth.get_balance(sender_address)}")
print(f"Final recipient balance: {web3.eth.get_balance(recipient_address)}")