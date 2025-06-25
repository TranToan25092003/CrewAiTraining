import unittest
from unittest.mock import patch

class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Withdrawal would result in negative balance.")
        self.balance -= amount
        self.transactions.append(f"Withdrew: {amount}")

    def buy_shares(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost > self.balance:
            raise ValueError("Not enough balance to buy shares.")
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(f"Bought {quantity} shares of {symbol} at {share_price} each.")

    def sell_shares(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")
        share_price = get_share_price(symbol)
        total_value = share_price * quantity
        self.balance += total_value
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append(f"Sold {quantity} shares of {symbol} at {share_price} each.")

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        initial_deposit = self.transactions[0].split(": ")[1] if self.transactions else 0
        return self.get_portfolio_value() - float(initial_deposit)

    def get_holdings(self) -> dict:
        return self.holdings

    def get_profit_or_loss_report(self) -> str:
        profit_or_loss = self.get_profit_or_loss()
        return f"Profit/Loss: {profit_or_loss}"

    def get_transaction_history(self) -> list:
        return self.transactions

def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test123', 1000.0)
    
    def test_initialization(self):
        self.assertEqual(self.account.account_id, 'test123')
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
    
    def test_deposit_positive_amount(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(self.account.transactions[-1], 'Deposited: 500.0')
    
    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)
    
    def test_deposit_zero_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
    
    def test_withdraw_positive_amount(self):
        self.account.withdraw(500.0)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(self.account.transactions[-1], 'Withdrew: 500.0')
    
    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)
    
    def test_withdraw_zero_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0.0)
    
    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500.0)
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_buy_shares(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 2))
        self.assertEqual(self.account.holdings, {'AAPL': 2})
        self.assertEqual(self.account.transactions[-1], 'Bought 2 shares of AAPL at 150.0 each.')
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_buy_shares_insufficient_funds(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 10)
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_buy_shares_zero_quantity(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 0)
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_shares(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 5)
        initial_balance = self.account.balance
        self.account.sell_shares('AAPL', 2)
        self.assertEqual(self.account.balance, initial_balance + (150.0 * 2))
        self.assertEqual(self.account.holdings, {'AAPL': 3})
        self.assertEqual(self.account.transactions[-1], 'Sold 2 shares of AAPL at 150.0 each.')
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_all_shares(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 5)
        self.assertEqual(self.account.holdings, {})
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_shares_not_owned(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.sell_shares('TSLA', 1)
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_shares_insufficient_quantity(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 2)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 3)
    
    @patch('__main__.get_share_price', side_effect=lambda x: {'AAPL': 150.0, 'TSLA': 800.0}.get(x, 0.0))
    def test_get_portfolio_value(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        expected_value = self.account.balance + (150.0 * 2) + (800.0 * 1)
        self.assertEqual(self.account.get_portfolio_value(), expected_value)
    
    def test_get_profit_or_loss(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        expected_profit = self.account.balance - 1000.0
        self.assertEqual(self.account.get_profit_or_loss(), expected_profit)
    
    @patch('__main__.get_share_price', return_value=150.0)
    def test_get_holdings(self, mock_get_share_price):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
    
    def test_get_profit_or_loss_report(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        expected_report = f"Profit/Loss: {self.account.get_profit_or_loss()}"
        self.assertEqual(self.account.get_profit_or_loss_report(), expected_report)
    
    def test_get_transaction_history(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        expected_history = ['Deposited: 500.0', 'Withdrew: 200.0']
        self.assertEqual(self.account.get_transaction_history(), expected_history)

class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_existing(self):
        self.assertEqual(get_share_price('AAPL'), 150.0)
        self.assertEqual(get_share_price('TSLA'), 800.0)
        self.assertEqual(get_share_price('GOOGL'), 2800.0)
    
    def test_get_share_price_non_existing(self):
        self.assertEqual(get_share_price('MSFT'), 0.0)

if __name__ == '__main__':
    unittest.main()