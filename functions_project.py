import json
from datetime import datetime
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
    if 'date' not in transaction:
        return "Invalid transaction: Missing 'date' field"

    date = datetime.strptime(transaction['date'], '%Y-%m-%dT%H:%M:%S.%f')
    formatted_date = date.strftime('%d.%m.%Y')
    formatted_transaction = f"{formatted_date} {transaction['description']}\n"
    if 'from' in transaction:
        formatted_transaction += f"{mask_card_number(transaction['from'])} -> {mask_account_number(transaction['to'])}\n"
    else:
        formatted_transaction += f"Счет -> {mask_account_number(transaction['to'])}\n"
    formatted_transaction += f"{transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}"
    return formatted_transaction


def display_last_transactions(transactions):
    sorted_transactions = sorted(transactions, key=lambda x: x.get('date', ''), reverse=True)
    last_transactions = sorted_transactions[:5]
    formatted_transactions = '\n'.join([format_transaction(transaction) for transaction in last_transactions])
    print(formatted_transactions)


