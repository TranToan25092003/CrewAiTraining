import gradio as gr
from accounts import Account

# Create an instance of the Account class
account = Account(account_id="user1", initial_deposit=1000.0)

def deposit_funds(amount):
    account.deposit(amount)
    return f"Deposited: {amount}, New Balance: {account.balance}"

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew: {amount}, New Balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}, New Balance: {account.balance}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}, New Balance: {account.balance}"
    except ValueError as e:
        return str(e)

def get_portfolio_value():
    value = account.get_portfolio_value()
    return f"Total Portfolio Value: {value}"

def get_profit_or_loss():
    profit_loss = account.get_profit_or_loss_report()
    return profit_loss

def get_holdings():
    holdings = account.get_holdings()
    return holdings

def get_transaction_history():
    transactions = account.get_transaction_history()
    return transactions

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("### Account Management System for Trading Simulation")
    
    with gr.Row():
        deposit = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
    
    deposit_button.click(fn=deposit_funds, inputs=deposit, outputs=deposit_button)

    with gr.Row():
        withdraw = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
    
    withdraw_button.click(fn=withdraw_funds, inputs=withdraw, outputs=withdraw_button)

    with gr.Row():
        buy_symbol = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
        buy_quantity = gr.Number(label="Quantity")
        buy_button = gr.Button("Buy Shares")
    
    buy_button.click(fn=buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_button)

    with gr.Row():
        sell_symbol = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
        sell_quantity = gr.Number(label="Quantity")
        sell_button = gr.Button("Sell Shares")
    
    sell_button.click(fn=sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_button)

    portfolio_value_button = gr.Button("Get Portfolio Value")
    portfolio_value_output = gr.Textbox(label="Portfolio Value", interactive=False)
    portfolio_value_button.click(fn=get_portfolio_value, outputs=portfolio_value_output)

    profit_loss_button = gr.Button("Get Profit/Loss")
    profit_loss_output = gr.Textbox(label="Profit/Loss", interactive=False)
    profit_loss_button.click(fn=get_profit_or_loss, outputs=profit_loss_output)

    holdings_button = gr.Button("Get Holdings")
    holdings_output = gr.Textbox(label="Holdings", interactive=False)
    holdings_button.click(fn=get_holdings, outputs=holdings_output)

    transactions_button = gr.Button("Get Transaction History")
    transactions_output = gr.Textbox(label="Transaction History", interactive=False)
    transactions_button.click(fn=get_transaction_history, outputs=transactions_output)

demo.launch()