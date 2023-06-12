import json
from datetime import datetime
def load_transactions(file_path):
    """
       Загружает данные о транзакциях из файла JSON.

       Args:
           file_path (str): Путь к файлу JSON.

       Returns:
           list: Список транзакций.

       Raises:
           FileNotFoundError: Если файл не найден.
           json.JSONDecodeError: Если возникает ошибка при декодировании JSON.

       """

    with open(file_path, 'r') as file:
        transactions_data = json.load(file)
    return transactions_data

def mask_card_number(card_number):
    """
       Маскирует номер карты, заменяя все цифры, кроме первых 4 и последних 4, символами "*".

       Args:
           card_number (str): Номер карты.

       Returns:
           str: Маскированный номер карты.

       """

    if ' ' in card_number:
        masked_number = card_number[:card_number.index(' ')]
        masked_number += ' ' + '*' * (len(card_number) - card_number.index(' ') - 1)
    else:
        masked_number = card_number[:4] + ' ' + '*' * (len(card_number) - 8) + card_number[-4:]
    return masked_number

def mask_account_number(account_number):
    """
       Маскирует номер счета, заменяя все цифры, кроме последних 4, символами "*".

       Args:
           account_number (str): Номер счета.

       Returns:
           str: Маскированный номер счета.

       """

    masked_number = '**' + account_number[-4:]
    return masked_number

def format_transaction(transaction):
    """
       Форматирует информацию о транзакции в заданном формате.

       Args:
           transaction (dict): Информация о транзакции.

       Returns:
           str: Отформатированная информация о транзакции.

       """

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
    """
     Выводит информацию о последних транзакциях.

     Args:
         transactions (list): Список транзакций.

     """


    sorted_transactions = sorted(transactions, key=lambda x: x.get('date', ''), reverse=True)
    last_transactions = sorted_transactions[:5]
    formatted_transactions = '\n'.join([format_transaction(transaction) for transaction in last_transactions])
    print(formatted_transactions)


