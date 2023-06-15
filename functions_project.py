import json
from datetime import datetime


def load_transactions(file_path):
    """
    Загружает транзакции из файла.

    Аргументы:
        file_path (str): Путь к файлу с транзакциями.

    Возвращает:
        list: Список транзакций в виде словарей.
    """
    with open(file_path, 'r') as file:
        transactions = json.load(file)
    return transactions


def mask_card_number(card_number):
    """
    Маскирует номер карты, оставляя видимыми только первые 6 и последние 4 цифры.

    Аргументы:
        card_number (str): Номер карты для маскировки.

    Возвращает:
        str: Замаскированный номер карты.
    """
    card_number = card_number.replace(" ", "")
    first_4 = card_number[:4]
    two_after = card_number[4:6]
    last_4 = card_number[-4:]
    return f"{first_4} {two_after}** **** {last_4}"


def mask_account_number(account_number):
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Аргументы:
        account_number (str): Номер счета для маскировки.

    Возвращает:
        str: Замаскированный номер счета.
    """
    return 'Счет **' + account_number[-4:]


def format_transaction(transaction):
    if 'from' not in transaction or 'to' not in transaction:
        raise Exception('Both "from" and "to" fields must be present')

    date_str = transaction.get('date', '').rstrip('Z')
    date = datetime.fromisoformat(date_str).strftime('%d.%m.%Y')

    description = transaction.get('description', '')
    from_info = transaction.get('from', '')
    to_info = transaction.get('to', '')
    amount = transaction.get('operationAmount', {}).get('amount', '')
    currency = transaction.get('operationAmount', {}).get('currency', {}).get('name', '')

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

    return f"{date} {description}\n{from_info} -> {to_info}\n{amount} {currency}\n"


def display_last_transactions(transactions):
    """
    Выводит последние 5 выполненных транзакций.

    Аргументы:
        transactions (list): Список транзакций для вывода.
    """
    executed_transactions = [t for t in transactions if
                             'state' in t and t['state'] == 'EXECUTED' and 'from' in t and 'to' in t]
    sorted_transactions = sorted(executed_transactions, key=lambda t: t['date'], reverse=True)
    for transaction in sorted_transactions[:5]:
        print(format_transaction(transaction))
        print()
