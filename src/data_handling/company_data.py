def get_company_data(company_name, revenue):
    return {
    # Financial Statement Items
    "reference": company_name,
    "revenue": revenue,
    "Cost of Goods Sold (COGS)/Cost of Materials": "Usually found directly in financial statements",
    "Gross Profit": "Gross Profit = Sales - COGS",
    "Operating Profits": "Operating Profit = Gross Profit - Operating Expenses",
    "Depreciation": "Usually found directly in financial statements",
    "Amortization": "Usually found directly in financial statements",
    "Earnings Before Taxes (EBT)": "EBT = Operating Profit - Interest Expense",
    "Net Income": "Net Income = EBT - Taxes",
    "Income Attributable to Shareholders of the Company": "Usually found directly in financial statements",
    "Interest Net (Interest Received - Interest Paid)": "Interest Net = Interest Received - Interest Paid",
    "Purchase Price Allocation (PPA)/Purchase Price Adjustment": "Not applicable (accounting adjustment)",

    # Cash Flow Statement
    "Operating Cash Flow": "Usually found directly in financial statements",
    "Capital Expenditures (CapEx)": "Usually found directly in financial statements",
    "Free Cash Flow (FCF)": "Free Cash Flow = Operating Cash Flow - CapEx",

    # Additional Useful Metrics
    "Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)": "EBITDA = Operating Profit + Depreciation + Amortization",
    "Compound Annual Growth Rate (CAGR)": "CAGR = (Ending Value / Beginning Value)^(1 / Number of Years) - 1",
    "Earnings Per Share (EPS)": "EPS = Net Income / Number of Outstanding Shares",
    "Dividend Per Share (DPS)": "DPS = Total Dividends Paid / Number of Outstanding Shares",
    "Return on Equity (ROE)": "ROE = Net Income / Shareholder's Equity",
    "Return on Assets (ROA)": "ROA = Net Income / Total Assets",
    "Return on Investment (ROI)": "ROI = (Net Profit / Cost of Investment) x 100",
    "Debt to Equity Ratio": "Debt to Equity Ratio = Total Debt / Shareholder's Equity",
    "Current Ratio": "Current Ratio = Current Assets / Current Liabilities",
    "Quick Ratio": "(Current Assets - Inventory) / Current Liabilities",
    "Interest Coverage Ratio": "Interest Coverage Ratio = Operating Profit / Interest Expense",
    "Free Cash Flow (FCF)": "FCF = Operating Cash Flow - CapEx",
    "Enterprise Value (EV)": "EV = Market Capitalization + Total Debt - Cash and Cash Equivalents",
    "Market Capitalization": "Market Cap = Share Price x Number of Outstanding Shares",
    "Book Value Per Share": "Book Value Per Share = Shareholder's Equity / Number of Outstanding Shares",
    "Working Capital": "Working Capital = Current Assets - Current Liabilities",
    "Inventory Turnover": "Inventory Turnover = COGS / Average Inventory",
    "Receivables Turnover": "Receivables Turnover = Net Credit Sales / Average Accounts Receivable",
    "Asset Turnover": "Asset Turnover = Sales / Average Total Assets",
    "Gross Margin Percentage": "Gross Margin % = (Gross Profit / Sales) x 100",
    "Operating Margin Percentage": "Operating Margin % = (Operating Profit / Sales) x 100",
    "Net Profit Margin Percentage": "Net Profit Margin % = (Net Income / Sales) x 100",
    "Beta (Volatility Measure)": "Not applicable (statistical measure)",

    # Debt and Equity Metrics
    "Total Debt": "Usually found directly in financial statements",
    "Long-Term Debt": "Usually found directly in financial statements",
    "Short-Term Debt": "Usually found directly in financial statements",
    "Equity Multiplier": "Equity Multiplier = Total Assets / Shareholder's Equity",
    "Dividend Yield": "Dividend Yield = (Annual Dividends Per Share / Price Per Share) x 100",

    # Valuation Ratios
    "Price to Earnings (P/E) Ratio": "P/E Ratio = Share Price / Earnings Per Share",
    "Price to Book (P/B) Ratio": "P/B Ratio = Share Price / Book Value Per Share",
    "Price to Sales (P/S) Ratio": "P/S Ratio = Share Price / (Sales / Number of Outstanding Shares)",
    "Price to Cash Flow (P/CF) Ratio": "P/CF Ratio = Share Price / (Operating Cash Flow / Number of Outstanding Shares)"
}

def create_revenue_entry(metric:str, value):
    return {'description': 'Usually found directly in financial statements', 'metric': metric, 'value': value}
