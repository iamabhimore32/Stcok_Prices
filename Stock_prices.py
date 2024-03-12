import pandas as pd
import matplotlib.pyplot as plt

def generate_signals(df):
    # Calculate moving averages
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    df['MA_500'] = df['Close'].rolling(window=500).mean()

    # Generate signals
    df['Signal_Buy'] = (df['MA_50'] > df['MA_500']) & (df['MA_50'].shift(1) <= df['MA_500'].shift(1))
    df['Signal_Sell'] = (df['MA_20'] < df['MA_200']) & (df['MA_20'].shift(1) >= df['MA_200'].shift(1))
    df['Signal_Close_Buy'] = (df['MA_10'] < df['MA_20']) & (df['MA_10'].shift(1) >= df['MA_20'].shift(1))
    df['Signal_Close_Sell'] = (df['MA_5'] > df['MA_10']) & (df['MA_5'].shift(1) <= df['MA_10'].shift(1))

def calculate_profit_loss(df):
    # Initialize positions
    df['Position'] = 0

    # Buy signals
    df.loc[df['Signal_Buy'], 'Position'] = 1

    # Sell signals
    df.loc[df['Signal_Sell'], 'Position'] = -1

    # Close buy positions
    df.loc[df['Signal_Close_Buy'], 'Position'] = 0

    # Close sell positions
    df.loc[df['Signal_Close_Sell'], 'Position'] = 0

    # Calculate daily returns
    df['Daily_Return'] = df['Close'].pct_change()

    # Calculate profit and loss
    df['Profit_Loss'] = df['Position'].shift(1) * df['Daily_Return']

    # Calculate cumulative profit and loss
    df['Cumulative_Profit_Loss'] = df['Profit_Loss'].cumsum()

def visualize_data(df):
    # Plotting
    plt.figure(figsize=(12, 8))
    plt.plot(df['Date'], df['Close'], label='Closing Price', linewidth=1)
    plt.scatter(df['Date'][df['Signal_Buy']], df['Close'][df['Signal_Buy']], marker='^', color='g', label='Buy Signal')
    plt.scatter(df['Date'][df['Signal_Sell']], df['Close'][df['Signal_Sell']], marker='v', color='r', label='Sell Signal')
    plt.title('Stock Price with Trading Signals')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.show()

    # Plot cumulative profit and loss
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Cumulative_Profit_Loss'], label='Cumulative Profit/Loss', color='b')
    plt.title('Cumulative Profit/Loss')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit/Loss')
    plt.legend()
    plt.show()

def main():
    # Load stock data into DataFrame
    df = pd.read_csv('stock_prices.csv')  # Replace with the path to your CSV file

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort DataFrame by date
    df = df.sort_values(by='Date')

    # Generate signals
    generate_signals(df)

    # Calculate profit and loss
    calculate_profit_loss(df)

    # Visualize data and signals
    visualize_data(df)

if __name__ == "__main__":
    main()
