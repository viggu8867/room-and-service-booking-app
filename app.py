import streamlit as st
import pymysql
import pandas as pd

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='Room'
)

session_state = st.session_state
privileges = session_state.get('privileges')

aggregate_query = """
SELECT r.ReservationID, r.CheckInDate, r.CheckOutDate, g.Name AS GuestName, SUM(p.Amount) AS TotalPayment
FROM Reservation r
JOIN Guest g ON r.GuestID = g.GuestID
LEFT JOIN Payments p ON r.ReservationID = p.ReservationID
GROUP BY r.ReservationID, r.CheckInDate, r.CheckOutDate, g.Name;
"""

def check_login(username, password):
    query = "SELECT Username, Privileges FROM User WHERE Username = %s AND Password = %s"
    cursor = connection.cursor()
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        username, privileges = result
        st.success("Login successful!")
        st.session_state['username'] = username
        st.session_state['privileges'] = privileges
        return True
    else:
        return False
    
def register_user(username, password, privileges):
    try:
        cursor = connection.cursor()
        if(privileges=="admin"):
            cursor.callproc('insert_admin_user', (username, password))
        else :
            query = "INSERT INTO User (Username, Password, Privileges) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, privileges))
        connection.commit()
        cursor.close()
        st.success("User registered successfully.")
    except pymysql.Error as err:
        st.error(f"Error: {err}")
        st.error("User registration failed.")

def execute_query(query, data=None, fetch=True):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        if fetch and cursor.description is not None:
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        connection.rollback()
        return pd.DataFrame()

def execute_nested_query(attribute):
    if attribute:
        nested_query = f"""
            SELECT GuestID, Name
            FROM Guest
            WHERE GuestID IN (
                SELECT DISTINCT g.GuestID
                FROM Guest g
                JOIN Reservation r ON g.GuestID = r.GuestID
                JOIN Room rm ON r.RoomNumber = rm.RoomNumber
                WHERE rm.RoomType = '{attribute}'
            )
        """
        nested_result = execute_query(nested_query)
        st.table(nested_result)
    else:
        st.warning("Please enter a Room Type.")

def display_entity(table_name):
    data = execute_query(f"SELECT * FROM {table_name}")
    st.table(data)

def insert_entity(entity_name, table_name, columns):
    st.subheader(entity_name)

    if(privileges=="admin"):
        st.subheader(f"Add a {entity_name} Entry")
        values = []
        for col_name, col_type in columns:
            if col_type == "int":
                values.append(st.number_input(f"{col_name}"))
            else:
                values.append(st.text_input(f"{col_name}"))
        
        if st.button(f"Add {entity_name}"):
            if all(values):
                query = f"INSERT INTO {table_name} ({', '.join([col[0] for col in columns])}) VALUES ({', '.join(['%s' for _ in columns])})"
                data = tuple(values)
                execute_query(query, data)
                st.success(f"{entity_name} added successfully!")
            else:
                st.error("Please fill in all fields.")
    else:
        st.error("User with standard privileges cannot insert data.")

def update_entity(entity_name, table_name, columns,primary_key):
    if(privileges=="admin"):
        st.subheader(f"Update a {entity_name} Entry")
        id_to_update = st.text_input(f"{primary_key} to update")
        if id_to_update:
            entry_to_update = execute_query(f"SELECT * FROM {table_name} WHERE {primary_key} = %s", (id_to_update,))
            if not entry_to_update.empty:
                update_values = []
                for col_name, col_type in columns:
                    if col_type == "int":
                        update_values.append(st.number_input(f"{col_name}", value=entry_to_update.iloc[0][col_name]))
                    else:
                        update_values.append(st.text_input(f"{col_name}", value=entry_to_update.iloc[0][col_name]))
                if st.button(f"Update {entity_name}"):
                    set_clause=','.join([f'{col_name} = %s' for col_name, _ in columns])
                    query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"
                    data = tuple([update_values[i] for i in range(len(columns))]+ [id_to_update])
                    execute_query(query, data)
                    st.success(f"{entity_name} updated successfully!")

            else:
                st.error(f"{entity_name} ID not found.")
    else:
        st.error("User with standard privileges cannot update data.")

def delete_entity(entity_name, table_name, columns,primary_key):
    if(privileges=="admin"):
        st.subheader(f"Delete a {entity_name} Entry")
        id_to_delete = st.text_input(f"{primary_key} to delete")
        if id_to_delete:
            if st.button(f"Delete {entity_name}"):
                execute_query(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (id_to_delete,))
                st.success(f"{entity_name} deleted successfully!")
    else:
        st.error("User with standard privileges cannot delete data.")

def join_tables(table1,table2,common_attribute):
    st.subheader("Join Tables")

    if st.button("Perform Join"):
        if table1 != table2:
            join_query = f"""
                SELECT *
                FROM {table1}
                NATURAL JOIN {table2}
            """
            join_result = execute_query(join_query)
            st.table(join_result)
        else:
            st.error("Cannot join the same table. Please select different tables.")

def display_all_users():
    st.subheader("All Users")
    query = "SELECT * FROM User"
    users = execute_query(query, fetch=True)
    st.table(users)

def delete_user(user_to_delete):
    if privileges == "admin":
        st.subheader("Delete User")
        table_name = "User"

        # Check if the user exists
        user_exists_query = f"SELECT * FROM {table_name} WHERE UserID = %s"
        user_exists_result = execute_query(user_exists_query, (user_to_delete,))

        if not user_exists_result.empty:
            # Check if the user has admin privileges
            admin_privilege_query = f"SELECT Privileges FROM {table_name} WHERE UserID = %s"
            result = execute_query(admin_privilege_query, (user_to_delete,))

            if result.iloc[0]["Privileges"] == "admin":
                st.error("Cannot delete a user with admin privileges.")
            else:
                if st.button("Delete User"):
                    execute_query(f"DELETE FROM {table_name} WHERE UserID = %s", (user_to_delete,))
                    st.success("User deleted successfully!")
        else:
            st.error(f"User with ID {user_to_delete} not found.")
    else:
        st.error("User with standard privileges cannot delete data.")

def change_role():
    if privileges == "admin":
        cursor = connection.cursor()
        st.subheader("Change User Role")
        user_to_change = st.text_input("Enter Username to change role:")
        
        new_role = st.selectbox("Select New Role:", ['admin', 'standard'])
        if(st.button("Change Role")):
            try:
                if user_to_change == st.session_state['username']:
                    st.error("Cannot change your own role.")
                    return 
                cursor = connection.cursor()
                cursor.callproc('grant_admin_role', (user_to_change, new_role))
                cursor.execute("UPDATE User SET Privileges = %s WHERE Username = %s", (new_role, user_to_change))
                connection.commit()
                cursor.close()
                st.success(f"User role changed to {new_role} successfully!")
            except pymysql.Error as err:
                st.error(f"Error: {err}")
                st.error("User role change failed.")
    else:
        st.error("User with standard privileges cannot change roles")

import datetime

def check_guest_details():
    st.title("Guest Stay Details")

    # Input fields for Date, Guest Name, and Phone Number
    selected_date = st.date_input("Select Date", datetime.date.today())
    guest_name = st.text_input("Enter Guest Name")
    phone_number = st.text_input("Enter Phone Number")

    if st.button("Check Stay Details"):
        stay_details_query = """
            SELECT r.ReservationID, r.CheckInDate, r.CheckOutDate, g.Name AS GuestName, rm.RoomNumber, b.ServiceID, s.ServiceName
            FROM Reservation r
            JOIN Guest g ON r.GuestID = g.GuestID
            JOIN Room rm ON r.RoomNumber = rm.RoomNumber
            LEFT JOIN Booking b ON r.ReservationID = b.ReservationID
            LEFT JOIN Service s ON b.ServiceID = s.ServiceID
            WHERE r.CheckInDate <= %s AND r.CheckOutDate >= %s AND g.Name = %s AND g.Phone = %s
        """

        stay_details_result = execute_query(stay_details_query, (selected_date, selected_date, guest_name, phone_number))

        if not stay_details_result.empty:
            st.subheader("Stay Details:")
            # st.table(stay_details_result[['ReservationID', 'CheckInDate', 'CheckOutDate', 'GuestName', 'RoomNumber']])
            st.dataframe(stay_details_result[['ReservationID', 'CheckInDate', 'CheckOutDate', 'GuestName', 'RoomNumber']].head(1))
            
            services_taken = stay_details_result[['ServiceID', 'ServiceName']].dropna().drop_duplicates()
            if not services_taken.empty:
                st.subheader("Services Taken:")
                st.table(services_taken)
            else:
                st.warning("No services taken during the stay.")
        else:
            st.warning("No records found for the given date, Guest Name, and Phone Number.")

st.title("Hotel Management System")

entity_info = [
    ("Guest", "Guest", [("GuestID", "text"), ("Name", "text"), ("Address", "text"), ("Phone", "text"), ("Age", "int")]),
    ("Room", "Room", [("RoomNumber", "int"), ("RoomType", "text"), ("Price", "float"), ("Availability", "text")]),
    ("Reservation", "Reservation", [("ReservationID", "text"), ("CheckInDate", "date"), ("CheckOutDate", "date"), ("GuestID", "text"), ("RoomNumber", "int")]),
    ("Staff", "Staff", [("StaffID", "text"), ("Name", "text"), ("Age", "int"), ("Position", "text"), ("Salary", "float")]),
    ("Service", "Service", [("ServiceID", "text"), ("ServiceName", "text"), ("ServicePrice", "float")]),
    ("Booking", "Booking", [("BookingID", "text"), ("ReservationID", "text"), ("ServiceID", "text"), ("Date", "date"), ("No_of_People", "int")]),
    ("Payments", "Payments", [("PaymentID", "text"), ("ReservationID", "text"), ("Amount", "float"), ("PaymentDate", "date"), ("PaymentMethod", "text")]),
    ("GuestFeedback", "GuestFeedback", [("FeedbackID", "text"), ("GuestID", "text"), ("Feedback", "text"), ("Rating", "text")])
]

is_authenticated = session_state.get('is_authenticated', False)

if not is_authenticated:
    st.title("Hotel Management System - Register")

    username = st.text_input("Username:", key="username_r")
    password = st.text_input("Password:", key="password_r",type="password")
    privileges = st.selectbox("Select Privileges:", ['admin', 'standard'])

    if st.button("Register"):
        register_user(username, password, privileges)

    st.title("Hotel Management System - Login")

    username = st.text_input("Username:", key="username_l")
    password = st.text_input("Password:", key="password_l", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.success("Login successful!")
            session_state['is_authenticated'] = True 
            st.rerun()  
        else:
            st.error("Invalid username or password.")
else:
    st.title("Hotel Management System - Home Page")
    selected_option = st.selectbox("Options", ["Home","User Management","Display","Insert", "Update", "Delete","Join","Payment detail for each reservation","Guest stay details"])

    if selected_option == "Display":
        selected_entity = st.selectbox("Select a table to view", [entity[0] for entity in entity_info])
        display_entity(selected_entity)

    if selected_option == "Insert":
        selected_entity = st.selectbox("Select an entity to insert", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                insert_entity(entity[0], entity[1], entity[2])

    elif selected_option == "Update":
        selected_entity = st.selectbox("Select an entity to update", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                primary_key = entity[-1][0][0]
                update_entity(entity[0], entity[1], entity[2],primary_key)
                
    elif selected_option == "Delete":
        selected_entity = st.selectbox("Select an entity to delete", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                primary_key = entity[-1][0][0]
                delete_entity(entity[0], entity[1], entity[2],primary_key)
        
    elif selected_option == "Join":
        table1 = st.selectbox("Select first entity to join", [entity[0] for entity in entity_info],key="table1")
        table2 = st.selectbox("Select second entity to join", [entity[0] for entity in entity_info],key="table2")
        common_attribute = st.text_input("Enter the common attribute for the join:")
        join_tables(table1,table2,common_attribute)

    elif selected_option == "Payment detail for each reservation" :
        st.subheader("Total Payments for Each Reservation")
        total_payment_result = execute_query(aggregate_query)
        st.table(total_payment_result)

    elif selected_option == "Guest stay details" :
        roomtype = st.selectbox("Select Room Type:",["Single Room","Double Room","Triple Room"])
        st.subheader(f"Guests who are staying in {roomtype}")
        guest_staying_result = execute_nested_query(roomtype)

    elif selected_option == "User Management":
        st.title("User Management")
        option=st.selectbox("Options",["Display Users","Delete User","Change Roles"])
        if option == 'Display Users':
            st.header("Users")
            display_all_users()
        elif option == "Delete User":
            user_to_delete=st.text_input("Enter UserID to be deleted:")
            delete_user(user_to_delete)
        elif option == "Change Roles":
            change_role()

    