from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Function to read the Excel file and return it as a DataFrame
def read_excel_file(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        return str(e)

@app.route('/')
def display_excel_data():
    excel_file_path = 'C:/Users/Sauli/Desktop/2. Vuosi/1. Moduuli/Design factory project/dokumentit/test.xlsx'  # Replace with your Excel file path
    df = read_excel_file(excel_file_path)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template('index.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True) 
