import sqlite3
import streamlit as st

# Connect to SQLite database or create it
conn = sqlite3.connect('app_database.db')
cursor = conn.cursor()

# Function to create a table
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      age INTEGER NOT NULL)''')
    conn.commit()

# Function to insert data into the table
def insert_user(name, age):
    cursor.execute('''INSERT INTO users (name, age) VALUES (?, ?)''', (name, age))
    conn.commit()

# Function to fetch all users
def view_users():
    cursor.execute('''SELECT * FROM users''')
    rows = cursor.fetchall()
    return rows

# Function to update a user's data
def update_user(user_id, name, age):
    cursor.execute('''UPDATE users SET name = ?, age = ? WHERE id = ?''', (name, age, user_id))
    conn.commit()

# Function to delete a user
def delete_user(user_id):
    cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    conn.commit()

# Streamlit UI
def main():
    st.title("SQLite Database Management with Streamlit")

    menu = ["Create Table", "Insert User", "View Users", "Update User", "Delete User"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Create Table
    if choice == "Create Table":
        if st.button("Create Table"):
            create_table()
            st.success("Table created successfully!")

    # Insert User
    elif choice == "Insert User":
        st.subheader("Insert User")
        name = st.text_input("Enter Name")
        age = st.number_input("Enter Age", min_value=1, max_value=100)
        if st.button("Insert"):
            insert_user(name, age)
            st.success(f"User {name} added successfully!")

    # View Users
    elif choice == "View Users":
        st.subheader("View Users")
        users = view_users()
        if users:
            for user in users:
                st.write(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
        else:
            st.info("No users found.")

    # Update User
    elif choice == "Update User":
        st.subheader("Update User")
        users = view_users()
        user_id_list = [user[0] for user in users]
        user_id = st.selectbox("Select User ID", user_id_list)
        name = st.text_input("Enter New Name")
        age = st.number_input("Enter New Age", min_value=1, max_value=100)
        if st.button("Update"):
            update_user(user_id, name, age)
            st.success(f"User {user_id} updated successfully!")

    # Delete User
    elif choice == "Delete User":
        st.subheader("Delete User")
        users = view_users()
        user_id_list = [user[0] for user in users]
        user_id = st.selectbox("Select User ID", user_id_list)
        if st.button("Delete"):
            delete_user(user_id)
            st.success(f"User {user_id} deleted successfully!")

if __name__ == '__main__':
    main()

    # Close the connection when done
    conn.close()
