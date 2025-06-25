class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        """
        Initializes an Account instance.
        
        :param account_id: A unique identifier for the account.
        :param initial_deposit: An initial amount to deposit into the account (default is 0.0).
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings = {}  # A dictionary to store share holdings (e.g., {'AAPL': quantity})
        self.transactions = []  # List to store transaction history

    def deposit(self, amount: float):
        """
        Deposits funds into the account.
        
        :param amount: The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount: float):
        """
        Withdraws funds from the account.

        :param amount: The amount to withdraw.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Withdrawal would result in negative balance.")
        
        self.balance -= amount
        self.transactions.append(f"Withdrew: {amount}")

    def buy_shares(self, symbol: str, quantity: int):
        """
        Buys shares of a stock.

        :param symbol: The stock symbol to buy shares of.
        :param quantity: The quantity of shares to buy.
        """
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
        """
        Sells shares of a stock.

        :param symbol: The stock symbol to sell shares of.
        :param quantity: The quantity of shares to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")
        
        share_price = get_share_price(symbol)
        total_value = share_price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]  # Remove the stock if no shares left
        
        self.transactions.append(f"Sold {quantity} shares of {symbol} at {share_price} each.")

    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.

        :return: Total portfolio value.
        """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.

        :return: Profit or loss amount.
        """
        initial_deposit = self.transactions[0].split(": ")[1] if self.transactions else 0
        return self.get_portfolio_value() - float(initial_deposit)

    def get_holdings(self) -> dict:
        """
        Reports the current holdings of the user.

        :return: A dictionary with stock symbols and their quantities.
        """
        return self.holdings

    def get_profit_or_loss_report(self) -> str:
        """
        Reports the profit or loss of the user at any point in time.

        :return: A string representation of the profit or loss.
        """
        profit_or_loss = self.get_profit_or_loss()
        return f"Profit/Loss: {profit_or_loss}"

    def get_transaction_history(self) -> list:
        """
        Lists all transactions that the user has made over time.

        :return: A list of transaction descriptions.
        """
        return self.transactions

def get_share_price(symbol: str) -> float:
    """
    Mock function to get the current price of a share.
    
    :param symbol: The stock symbol for which to get the share price.
    :return: The current share price.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)