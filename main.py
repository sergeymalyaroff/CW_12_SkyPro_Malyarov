from functions_project import load_transactions, mask_card_number, mask_account_number, format_transaction, \
    display_last_transactions


def main():
    file_path = 'operations.json'
    transactions_data = load_transactions(file_path)
    transactions = transactions_data
    display_last_transactions(transactions)


if __name__ == '__main__':
    main()
