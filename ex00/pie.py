import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def main():
    try:
        # Connection parameters
        db_user = 'mmaekawa'
        db_password = 'mysecretpassword'
        db_host = 'localhost'
        db_port = '5433' # 5432に変更する
        db_name = 'piscineds'

        # Create connection string
        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Create SQLAlchemy engine
        engine = create_engine(connection_string)

        # Query the data
        query = "SELECT event_type, COUNT(*) as count FROM customers GROUP BY event_type"
        df = pd.read_sql(query, engine)

        # Check if dataframe is not empty
        if df.empty:
            print("No data found in customers table.")
            return

        # Sort by count in descending order
        df = df.sort_values(by='count', ascending=False)

        # Create pie chart
        plt.figure(figsize=(10, 10))
        plt.pie(
            df['count'], 
            labels=df['event_type'], 
            autopct='%1.1f%%',
            textprops={'fontsize': 16},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        # Save the plot
        output_file = 'pie.png'
        plt.savefig(output_file)
        print(f"Pie chart saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
