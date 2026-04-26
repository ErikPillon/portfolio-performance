import pandas as pd
from dataclasses import dataclass

@dataclass
class PortfolioMetrics:
    total_deposits: float
    total_withdrawals: float
    total_expenses: float
    total_dividends_interest: float
    net_invested_in_assets: float
    cash_balance: float
    net_investable_capital: float

class TradeRepublicParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self._load_and_clean_data()
        self._categorize_transactions()

    def _load_and_clean_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)
        # Filter to only executed transactions
        df = df[df['status'] == 'executed'].copy()
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['subtitle'] = df['subtitle'].fillna('')
        df['title'] = df['title'].fillna('')
        return df

    def _categorize_transactions(self):
        # Default category is Expenses for anything negative that isn't an investment or withdrawal
        self.df['category'] = 'Expenses'
        
        # Deposits and Withdrawals (identified by my name)
        name_mask = self.df['title'].str.contains('Erik Pillon|PILLON ERIK', case=False, na=False)
        self.df.loc[name_mask & (self.df['value'] > 0), 'category'] = 'Deposits'
        self.df.loc[name_mask & (self.df['value'] < 0), 'category'] = 'Withdrawals'

        # Investments (Buys, Sells, Savings)
        investment_mask = self.df['subtitle'].str.contains('Saving executed|Buy Order|Sell Order', case=False, na=False)
        self.df.loc[investment_mask, 'category'] = 'Investments'

        # Dividends and Interests
        dividend_mask = (self.df['subtitle'].str.contains('Cash dividend|Interest payment|Fixed Interest|Bonus', case=False, na=False) |
                         self.df['title'].str.contains('Interest', case=False, na=False))
        self.df.loc[dividend_mask, 'category'] = 'Dividends_Interests'
        
        # Fix category for positive values that aren't categorized properly yet (just in case)
        # If there's a positive value that is not a Deposit, Dividend/Interest or Sell Order, we don't want it in Expenses
        positive_uncategorized = (self.df['value'] > 0) & (self.df['category'] == 'Expenses')
        self.df.loc[positive_uncategorized, 'category'] = 'Other_Income'

    def get_metrics(self) -> PortfolioMetrics:
        grouped = self.df.groupby('category')['value'].sum()
        
        deposits = grouped.get('Deposits', 0.0)
        withdrawals = grouped.get('Withdrawals', 0.0)
        expenses = grouped.get('Expenses', 0.0) # This is negative
        dividends_interest = grouped.get('Dividends_Interests', 0.0)
        net_invested = grouped.get('Investments', 0.0) # This is negative if more buys than sells
        
        # Net investable capital is the cash actually intended for investing 
        # (Total Deposits + Total Withdrawals + Total Expenses)
        # Note: withdrawals and expenses are negative, so we add them
        net_investable_capital = deposits + withdrawals + expenses

        # Theoretical cash balance = net_investable_capital + net_invested + dividends_interest
        # (Net invested is negative, so adding it reduces cash)
        cash_balance = net_investable_capital + net_invested + dividends_interest
        
        return PortfolioMetrics(
            total_deposits=deposits,
            total_withdrawals=withdrawals,
            total_expenses=abs(expenses),
            total_dividends_interest=dividends_interest,
            net_invested_in_assets=abs(net_invested),
            cash_balance=cash_balance,
            net_investable_capital=net_investable_capital
        )

    def get_transactions_by_category(self, category: str) -> pd.DataFrame:
        return self.df[self.df['category'] == category].sort_values(by='timestamp', ascending=False)
