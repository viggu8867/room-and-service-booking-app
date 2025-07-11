
# 🏨 Room and Service Booking App

An integrated, real-time **Hotel Management System** built using **Python (Streamlit)** and **MySQL**, enabling secure and efficient handling of hotel operations like guest bookings, room and staff management, services, payments, and user privileges.

## 👨‍💻 Team Members
- Vignesh Madivala (PES1UG22AM190)
- Shashank Bellad (PES1UG22AM150)

---

## 📌 Project Description

This application simulates a real-time hotel environment, allowing:
- Guests to book rooms and services
- Staff to manage operations
- Admins to enforce access control via privilege-based user roles

It combines **frontend interactivity with backend automation**, including:
- CRUD operations
- Nested queries
- Triggers
- Stored procedures
- Admin limitations and validations

---

## 🧰 Tech Stack

### 🔗 Frontend
- [Streamlit](https://streamlit.io): Interactive Python web framework
- `pandas`: For data handling and display

### 🗄️ Backend
- **MySQL**: For structured relational data
- `PyMySQL`: Python-MySQL connector

### 💻 Development Tools
- MySQL Workbench / CLI
- Python IDE (VS Code / PyCharm)
- Web browser for Streamlit app

---

## 🧠 Core Functionalities

### 🔐 User Management
- Admin and standard roles
- Registration with admin restriction (max 3)
- User login/logout
- Role-based access control (RBAC)
- Dynamic role change (with protection against deleting the last admin)

### 🏨 Entity Management (CRUD)
Fully supports creation, update, deletion, and display of:
- Guests
- Rooms
- Reservations
- Staff
- Services
- Bookings
- Payments
- Guest Feedback

### 📊 SQL Operations Implemented
- **Nested Queries**: To find guests by room type
- **Join Queries**: For combining reservation, payment, and guest info
- **Stored Procedures**:
  - `insert_admin_user`: Limits admin users to 3
  - `grant_admin_role`: Safely reassigns user roles
- **Triggers**:
  - Auto-update room availability on insert/update/delete of reservations

### 💵 Payment Aggregation
- Calculates and displays **total payments per reservation**

### 🧾 Guest Stay Detail
- Retrieves guest stay and service history using **date, name, and phone** filters

---

## 🗃️ Database Schema

- 9 interrelated tables (`Guest`, `Room`, `Reservation`, `Staff`, `Service`, `Booking`, `Payments`, `GuestFeedback`, `User`)
- Relational constraints (PKs, FKs)
- Enum validation for availability, rating, and payment methods
- Trigger-based status updates for room availability

---

