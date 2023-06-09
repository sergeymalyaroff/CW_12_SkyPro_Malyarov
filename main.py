import json

def load_transactions(file_path):
    with open(file_path, 'r') as file:
        transactions_data = json.load(file)
    return transactions_data

def mask_card_number(card_number):
    masked_number = card_number[:4] + ' ' + ' '.join(['*' * 2 + card_number[i:i+4] for i in range(4, len(card_number), 4)])
    return masked_number

def mask_account_number(account_number):
    masked_number = '**' + account_number[-4:]
    return masked_number

def format_transaction(transaction):
    formatted_transaction = f"{transaction['date']} {transaction['description']}\n"
    if 'from' in transaction:
        formatted_transaction += f"{mask_card_number(transaction['from'])} -> {transaction['to']}\n"
    else:
        formatted_transaction += f"Счет -> {transaction['to']}\n"
    formatted_transaction += f"{transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}"
    return formatted_transaction

def display_last_transactions(transactions):
    last_transactions = transactions[-5:]
    formatted_transactions = '\n'.join([format_transaction(transaction) for transaction in last_transactions])
    print(formatted_transactions)

file_path = 'operations.json'
transactions_data = load_transactions(file_path)
transactions = transactions_data  # Обратите внимание на изменение этой строки
display_last_transactions(transactions)




