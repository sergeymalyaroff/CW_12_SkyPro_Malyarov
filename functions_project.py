import json
from datetime import datetime

def load_transactions(file_path):
    with open(file_path, 'r') as file:
        transactions = json.load(file)
    return transactions

def mask_card_number(card_number):
    card_number = card_number.replace(" ", "")
    first_6 = card_number[:6]
    last_4 = card_number[-4:]
    return f"{first_6} **** **** {last_4}"


def mask_account_number(account_number):
    return 'Счет **' + account_number[-4:]

def format_transaction(transaction):
    date = datetime.strptime(transaction['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    description = transaction['description']
    from_info = transaction.get('from')
    to_info = transaction.get('to')
    amount = transaction['operationAmount']['amount']
    currency = transaction['operationAmount']['currency']['name']

    if from_info and ' ' in from_info:
        from_parts = from_info.split(' ')
        if from_parts[0] == 'Счет':
            from_info = mask_account_number(from_parts[1])
        else:
            from_info = ' '.join(from_parts[:-1]) + ' ' + mask_card_number(from_parts[-1])
    elif from_info:
        from_info = mask_account_number(from_info)

    if to_info and ' ' in to_info:
        to_parts = to_info.split(' ')
        if to_parts[0] == 'Счет':
            to_info = mask_account_number(to_parts[1])
        else:
            to_info = ' '.join(to_parts[:-1]) + ' ' + mask_card_number(to_parts[-1])
    elif to_info:
        to_info = mask_account_number(to_info)

    return f"{date} {description}\n{from_info if from_info else ''} -> {to_info if to_info else ''}\n{amount} {currency}\n"


def display_last_transactions(transactions):
    executed_transactions = [t for t in transactions if 'state' in t and t['state'] == 'EXECUTED']
    sorted_transactions = sorted(executed_transactions, key=lambda t: t['date'], reverse=True)
    for transaction in sorted_transactions[:5]:
        print(format_transaction(transaction))
        print()
