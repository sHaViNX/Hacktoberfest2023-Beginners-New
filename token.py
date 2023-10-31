import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import spacy
import mysql.connector

# Load your trained model
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
model = BertForSequenceClassification.from_pretrained("/content/trained_model")

# Load your dataset
dataset_path = "/content/dataset3.csv"
df = pd.read_csv(dataset_path)

query_type_column = 'Query_type'
query_column = 'Query'
response_column = 'Answer'

# Load the SpaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Define a function to extract book titles
def extract_book_title(user_query):
    doc = nlp(user_query)
    book_titles = []

    for ent in doc.ents:
        if ent.label_ == "BOOK":
            book_titles.append(ent.text)

    return book_titles

# Define a function to check book availability in the MySQL database
def check_book_availability(book_title):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="book_list"
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Query the database to check book availability
        query = f"SELECT availability FROM books WHERE title = '{book_title}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            availability = result[0]
            if availability == 1:
                return "Yes, the book is available."
            else:
                return "No, the book is not available at the moment."
        else:
            return f"Sorry, we couldn't find information about the book '{book_title}' in our database."

    except Exception as e:
        print("Error:", e)
        return "An error occurred while checking the book availability."

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ...

while True:
    user_query = input("Enter Your Query (type 'exit' to quit): ")

    # Check if the user wants to exit
    if user_query.lower() == 'exit':
        print("Goodbye!")
        break  # Exit the loop

    e query_type
    predicted_query_type = None
    for query_type, label in query_type_to_label.items():
        if label == predicted_label:
            predicted_query_type = query_type
            break

    if predicted_query_type == "Book Availability":
        # Extract book titles more robustly
        book_titles = extract_book_title(user_query)

        if book_titles:
            # Assuming there can be multiple book titles in the query
            response = "\n".join([check_book_availability(title) for title in book_titles])
        else:
            response = "Sorry, we couldn't identify any book titles in your query."
    else:
        # For other query types, use the dataset response
        response = df[df[query_type_column] == predicted_query_type][response_column].iloc[0]

    print(f"User Query: {user_query}")
    print(f"Predicted Query Type: {predicted_query_type}")
    print(f"Response: {response}")
