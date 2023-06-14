import pytest
from functions_project import mask_card_number, mask_account_number, format_transaction, load_transactions

def test_mask_card_number():
    card_number = "1234567890123456"
    assert mask_card_number(card_number) == "123456 **** **** 3456"

def test_mask_account_number():
    account_number = "1234567890123456"
    assert mask_account_number(account_number) == "Счет **3456"

def test_format_transaction():
    transaction = {
        "date": "2023-06-30T14:15:22.123456",
        "description": "Test operation",
        "from": "Visa Classic 1234567890123456",
        "to": "Счет 1234567890123456",
        "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
    }
    expected_output = (
        "30.06.2023 Test operation\n"
        "Visa Classic 123456 **** **** 3456 -> Счет **3456\n"
        "100.00 USD\n"
    )
    assert format_transaction(transaction) == expected_output

def test_load_transactions():
    transactions = load_transactions("path_to_test_file.json")
    assert len(transactions) > 0
    assert "date" in transactions[0]
    assert "description" in transactions[0]
    assert "from" in transactions[0]
    assert "to" in transactions[0]
    assert "operationAmount" in transactions[0]
    assert "amount" in transactions[0]["operationAmount"]
    assert "currency" in transactions[0]["operationAmount"]

def test_format_transaction_with_different_types():
    transaction = {
        "date": "2023-06-30T14:15:22.123456",
        "description": "Перевод организации",
        "from": "Счет 1234567890123456",
        "to": "Visa Classic 1234567890123456",
        "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
    }
    expected_output = (
        "30.06.2023 Перевод организации\n"
        "Счет **3456 -> Visa Classic 123456 **** **** 3456\n"
        "100.00 USD\n"
    )
    assert format_transaction(transaction) == expected_output


