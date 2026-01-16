# 🛒 JustKart – Multi-User Inventory Management System

JustKart is a full-stack, multi-user inventory management web application built using **FastAPI**, **Streamlit**, and **PostgreSQL**.  
It allows multiple users to securely register, log in, and manage their own inventory independently.

Each user sees **only their own products**, ensuring proper data isolation and security.

---

## 🚀 Features

- 🔐 User Authentication (Register & Login)
- 👤 Multi-User Support with Data Isolation
- 📦 Add, Update, Delete Inventory Items
- 📊 Cart Summary (Total Products, Quantity, Value)
- 🔍 Search Products by Name
- 🧠 Secure Password Hashing (bcrypt)
- ☁️ PostgreSQL Database
- 🎨 Clean & Interactive Streamlit UI

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Passlib (bcrypt)
- Uvicorn

### Frontend
- Streamlit
- Requests
- Pandas

---

## 🏗️ Project Structure

```
JustKart/
│
├── backend/
│   ├── main.py
│   ├── databases.py
│   ├── databasemodels.py
│   ├── models_db.py
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit.py
│   └── requirements.txt
│
└── README.md
```

---

## 🔐 Authentication Flow

1. User registers with username & password
2. Password is securely hashed using bcrypt
3. User logs in
4. Session is managed using Streamlit session_state
5. Inventory items are linked to the logged-in user
6. Users can only access their own data

---

## 📦 Inventory Logic

- Each product is stored with a user_id
- Backend filters products using logged-in user
- Complete data isolation between users

---

## ▶️ Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL:
```
http://127.0.0.1:8000
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit.py
```

Frontend URL:
```
http://localhost:8501
```

---

## 🗄️ Database Configuration

Set PostgreSQL URL as environment variable:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
```

Tables are auto-created on backend startup.

---

## 🌐 Deployment

This project can be deployed on **Render** using:
- FastAPI backend service
- Streamlit frontend service
- Managed PostgreSQL database

---

## 📌 Future Enhancements

- JWT Authentication
- Role-based access (Admin/User)
- Product categories
- Inventory analytics
- Cloud deployment with custom domain

---

## 👨‍💻 Author

**Anurag**    
Aspiring Backend & Full-Stack Developer

---

⭐ If you like this project, consider giving it a star on GitHub!
