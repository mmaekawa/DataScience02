import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import matplotlib.dates as mdates

def main():
    try:
        # Connection parameters
        db_user = 'mmaekawa'
        db_password = 'mysecretpassword'
        db_host = 'localhost'
        db_port = '5433'
        db_name = 'piscineds'

        # Create connection string
        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Create SQLAlchemy engine
        engine = create_engine(connection_string)

        # Query the data for event_type 'purchase' between 2022-10 and 2023-02
        query = """
        SELECT event_time, price, user_id 
        FROM customers 
        WHERE event_type = 'purchase' 
        AND event_time >= '2022-10-01' 
        AND event_time < '2023-03-01'
        """
        df = pd.read_sql(query, engine)

        if df.empty:
            print("No data found for the specified period.")
            return

        # Ensure event_time is datetime
        df['event_time'] = pd.to_datetime(df['event_time'])
        
        # Create separate date column for daily grouping
        df['date'] = df['event_time'].dt.date
        df['month_period'] = df['event_time'].dt.to_period('M')

        # 1. Customer transition (Daily unique customers)
        daily_customers = df.groupby('date')['user_id'].nunique()

        # 2. Monthly total sales
        monthly_sales = df.groupby('month_period')['price'].sum()

        # 3. Daily average customer payment (Daily Total Revenue / Daily Unique Customers)
        daily_revenue = df.groupby('date')['price'].sum()
        daily_avg_payment = daily_revenue / daily_customers

        # --- Plot 1: Customer Transition (Line) ---
        plt.figure(figsize=(10, 6))
        plt.gca().set_facecolor('lavender')
        plt.plot(daily_customers.index, daily_customers.values)
        plt.xlabel('month')
        plt.ylabel('Number of customers')
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator()) # 月ごとに目盛りを設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b')) # %bは月を短縮形で表示するフォーマットコード
        plt.grid(True, color='white')
        plt.gca().set_axisbelow(True) # グリッドを背面へ
        plt.tight_layout()
        plt.savefig('customers.png')
        plt.close()
        print("Created customers.png")

        # --- Plot 2: Monthly Total Sales (Bar) ---
        plt.figure(figsize=(10, 6))
        plt.gca().set_facecolor('lavender')
        month_labels = [m.strftime('%b') for m in monthly_sales.index]
        plt.bar(month_labels, monthly_sales.values, color='lightsteelblue')
        plt.xlabel('month')
        plt.ylabel('Total sales in million of ₳')
        plt.grid(axis='y', color='white')
        plt.gca().set_axisbelow(True) # グリッドを背面へ
        plt.tight_layout()
        plt.savefig('sales.png')
        plt.close()
        print("Created sales.png")

        # --- Plot 3: Daily Average Customer Payment (Area/Line) ---
        plt.figure(figsize=(10, 6))
        plt.gca().set_facecolor('lavender')
        plt.fill_between(daily_avg_payment.index, daily_avg_payment.values, color='lightsteelblue')
        plt.xlabel('month')
        plt.ylabel('Average spend/customers in ₳')
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator()) # 月ごとに目盛りを設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b')) # %bは月を短縮形で表示するフォーマットコード
        plt.grid(True, color='white')
        plt.gca().set_axisbelow(True) # グリッドを背面へ
        plt.tight_layout()
        plt.savefig('average_spend.png')
        plt.close()
        print("Created average_spend.png")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
