import unittest
from functions_project import mask_card_number, mask_account_number

class TestFunctions(unittest.TestCase):

    def test_mask_card_number(self):
        card_number = 'Visa Gold 5999414228426353'
        masked_number = mask_card_number(card_number)
        self.assertEqual(masked_number, 'Visa Gold ************6353')

        card_number = 'MasterCard 3152479541115065'
        masked_number = mask_card_number(card_number)
        self.assertEqual(masked_number, 'MasterCard ****************5065')

        card_number = 'Maestro 3928549031574026'
        masked_number = mask_card_number(card_number)
        self.assertEqual(masked_number, 'Maestro ****************4026')

    def test_mask_account_number(self):
        account_number = 'Счет 72731966109147704472'
        masked_number = mask_account_number(account_number)
        self.assertEqual(masked_number, 'Счет **************7472')

        account_number = 'Счет 84163357546688983493'
        masked_number = mask_account_number(account_number)
        self.assertEqual(masked_number, 'Счет **************3493')

        account_number = 'Счет 17066032701791012883'
        masked_number = mask_account_number(account_number)
        self.assertEqual(masked_number, 'Счет **************2883')

if __name__ == '__main__':
    unittest.main()
