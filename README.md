# BudgetPal 💰

BudgetPal is a comprehensive, modern expense planner and financial tracker designed for personal budgeting and seamless group expense splitting. Built with a sleek, glassmorphic UI, it helps users take control of their finances effortlessly.

## 🚀 Key Features

* **Personal Financial Dashboard**: Track incomes, set budgets, and monitor categorized personal expenses.
* **Smart Group Splitting**: Create groups, add friends via email, and add shared expenses. The application utilizes a highly optimized settlement algorithm (resolving debts in integer cents to prevent floating-point inaccuracies) to calculate exactly who owes whom.
* **Real-time Analytics**: Visual spending trends and income vs. expense charts.
* **Secure Authentication**: Firebase-backed Google OAuth login and strictly protected backend endpoints.
* **Scalable Architecture**: Batched Firebase Auth fetching and properly indexed Firestore queries ensure high performance.

## 🛠 Tech Stack

* **Frontend:** Vanilla HTML, CSS, JavaScript (ES6), TailwindCSS, Chart.js.
* **Backend:** Python, Flask, Firebase Admin SDK.
* **Database & Auth:** Google Firebase (Firestore Database, Firebase Authentication).

---

## 💻 Local Setup & Installation

Follow these steps to clone and run the project locally for future improvements.

### 1. Clone the Repository
```bash
git clone https://github.com/Suthish-S-lone/Budgetpal.git
cd Budgetpal
```

### 2. Configure Firebase Setup
Because sensitive keys are excluded from Git, you must provide your own Firebase configuration:

1. **Frontend (`frontend/config.js`)**:
   Create this file to hold your Firebase Web API config. (Use `config.example.js` as a template if available).
2. **Backend (`backend/serviceAccountKey.json`)**:
   Generate a new private key from your Firebase project settings (Service Accounts tab) and save it in the `backend/` folder.
3. **Backend Environment (`backend/.env`)**:
   Create a `.env` file referencing the key:
   ```env
   FLASK_ENV=development
   PORT=5000
   GOOGLE_APPLICATION_CREDENTIALS=./serviceAccountKey.json
   ```

### 3. Start the Backend Server
Requires Python 3.10+ installed.

```bash
cd backend
# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate.bat   # (Windows)
# source venv/bin/activate    # (Mac/Linux)

# Install dependencies
pip install -r requirements.txt

# Start the Flask API
python app.py
```
*The backend will run on `http://127.0.0.1:5000`.*

### 4. Start the Frontend Server
Open a new terminal window.

```bash
cd frontend
# Start a simple local web server
python -m http.server 3000
```
*Open `http://localhost:3000` in your web browser to view the application.*

### 5. Deploy Firestore Indexes
The application utilizes compound queries that require Firestore indexes. Deploy them using the Firebase CLI:
```bash
firebase deploy --only firestore:indexes
```

---

## 🗺 Future Improvement Roadmap

This repository was heavily optimized, but the following enhancements are planned for the future:

1. **Dedicated Landing Page (UX)**: Introduce a dedicated, beautiful landing page (hiding the main dashboard layout) for unauthenticated visitors to improve the onboarding experience.
2. **Frontend Modularization**: Refactor the monolithic `index.html` file into dedicated ES6 Javascript modules (`api.js`, `auth.js`, `settlement.js`, `app.js`).
3. **Automated Testing**: Introduce `pytest` for the backend Flask routes and `Jest`/`Vitest` for validating frontend Split-Wise mathematics.
4. **Token Refresh Interceptors**: Implement automatic background Firebase token refreshing before making backend API requests to prevent silent expiration timeouts.

---
*Created and maintained by [Suthish-S-lone](https://github.com/Suthish-S-lone)*
