import json
import pytest
import datetime
from datetime import datetime
from functions_project import (
    load_transactions,
    mask_card_number,
    mask_account_number,
    format_transaction,
    display_last_transactions,
)


def test_load_transactions(tmp_path):
    data = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2022-01-01T12:00:00.000Z",
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Test Transaction",
            "from": "Account 1234567890",
            "to": "Account 0987654321"
        }
    ]
    file_path = tmp_path / "transactions.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    transactions = load_transactions(file_path)
    assert transactions == data


def test_mask_card_number():
    card_number = "Visa Classic 2842 8765 9012"
    masked_number = mask_card_number(card_number)
    assert masked_number == "Visa Cl** **** 9012"


def test_mask_account_number():
    account_number = "Account 1234567890"
    masked_number = mask_account_number(account_number)
    assert masked_number == "Счет **7890"


""" -------- """


@pytest.mark.parametrize(
    "transaction, expected_result",
    [

        (
                {
                    "date": "2019-07-03T18:35:29.512364Z",
                    "description": "Перевод на счет",
                    "from": "Счет 66666666666666666666",
                    "to": "Visa 1234567890123456",
                    "operationAmount": {
                        "amount": "8221.37",
                        "currency": {
                            "name": "USD",
                            "code": "USD"
                        }
                    },
                },
                "03.07.2019 Перевод на счет\nСчет **6666 -> Visa 1234 56** **** 3456\n8221.37 USD\n",
        ),
    ],
)
def test_format_transaction(transaction, expected_result):
    assert format_transaction(transaction) == expected_result


@pytest.mark.parametrize(
    "transaction",
    [
        (
                {
                    "date": "2019-07-03T18:35:29.512364Z",
                    "description": "Перевод на счет",
                    "from": "Счет 66666666666666666666",
                    "operationAmount": {
                        "amount": "8221.37",
                        "currency": {
                            "name": "USD",
                            "code": "USD"
                        }
                    },
                }
        ),
        (
                {
                    "date": "2019-08-26T10:50:58.294041Z",
                    "description": "Перевод организации",
                    "to": "Счет 64686473678894779589",
                    "operationAmount": {
                        "amount": "31957.58",
                        "currency": {
                            "name": "руб.",
                            "code": "RUB"
                        }
                    },
                }
        ),
    ],
)
def test_format_transaction_no_to_from(transaction):
    with pytest.raises(Exception, match='Both "from" and "to" fields must be present'):
        assert format_transaction(transaction)
