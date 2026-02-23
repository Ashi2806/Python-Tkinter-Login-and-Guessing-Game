# 1.Project Title
## Tkinter Login System & Number Guessing Game (Python + SQLite)

# 2.Overview
A Python desktop application built with Tkinter and SQLite that provides user sign-up and login, an interactive number guessing game, and a leaderboard based on minimum attempts. The project demonstrates GUI development, database integration, input validation, and event-driven programming in Python.

# 3.Features
- 📝 User registration (Sign up)
- 🔑 User login authentication
- 📱 Input validation for phone number and password
- 🎲 Random number guessing game
- 🎯 Attempts tracking
- 🏆 Leaderboard based on minimum attempts
- 💾 SQLite database storage

# 4.Application Flow
- 📂 User opens the application  
- 🔑 User logs in or creates a new account  
- ✅ After successful login, the game screen opens  
- 🎲 User selects a range and starts guessing  
- 🎯 Attempts are counted  
- 💾 Results are stored in the database  
- 🏆 Leaderboard can be viewed after winning  

# 5.Validations Implemented

### 📱 Phone Number
- Must contain only digits  
- Must be exactly 10 digits  
- Must start with digits 6–9  

### 🔑 Password
- Must contain both letters and digits  
- Must have at least 6 characters  

### 🚫 Duplicate Checks
- Duplicate phone numbers are not allowed  
- Duplicate usernames are prevented  

# 6.Technologies Used
-Python
-Tkinter (GUI)
-SQLite (Database)
