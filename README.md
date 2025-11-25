# Chemical Equipment Parameter Visualizer

A hybrid **Web + Desktop application** for visualizing and analyzing chemical equipment parameters.  
This tool helps users explore, monitor, and interpret chemical datasets through interactive charts, tables, and analytics.

---

## 📌 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Contact](#contact)

---

## 🚀 Features
- Upload and manage chemical datasets  
- Interactive visualizations (charts, graphs, tables)  
- Multi-platform support (web & desktop)  
- Real-time data view (if backend supports it)  
- Export charts and analysis reports  

---

## 🛠 Technologies Used
**Frontend:** React.js, Axios, Recharts, HTML5, CSS  
**Backend:** Django / Flask (choose depending on your implementation)  
**Database:** SQLite  
**Tools:** Webpack, npm  
**Version Control:** Git & GitHub  
**Desktop Build:** Electron.js (optional)

---

## ⚙️ Installation

### **1. Clone the Repository**
git clone https://github.com/Akanksh0301/Chemical-visualizer.git

cd chemical-visualizer


---

## **Frontend Setup**

cd chemical-visualizer-frontend
npm install # Install dependencies
npm start # Runs frontend at http://localhost:3000


If you get polyfill/webpack errors (common in React apps):
npm install stream-http https-browserify stream-browserify util browserify-zlib url assert


---

## **Backend Setup**
cd ../backend
pip install -r requirements.txt # Install Python dependencies
python manage.py migrate # Apply database migrations
python manage.py runserver # Start backend


Backend runs at:  
👉 http://127.0.0.1:8000/

---

## ▶️ Usage
1. Start backend + frontend  
2. Open the frontend: http://localhost:3000  
3. Go to **Upload Page** → Upload CSV chemical dataset  
4. Go to **History Page / Detail Page** → View visualizations  
5. Export charts or data  
6. (Optional) Real-time monitoring if backend supports streams  

---

## 📂 Project Structure

chemical-visualizer/
├── backend/ # Backend code (Django/Flask)
│ ├── db.sqlite3
│ ├── media/uploads/
│ │ └── ...
│ └── ...
│
├── chemical-visualizer-frontend/ # Frontend React App
│ ├── node_modules/
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── README.md
│
├── backend.zip # Optional backup (ignored by git)
├── bfg-1.15.0.jar # Optional cleanup tool
└── README.md # This file

---

## 🤝 Contributing

We welcome contributions!

1. **Fork** the repository  
2. Create a new branch:
git checkout -b feature/your-feature-name
3. Make your changes and commit:
git commit -m "Add feature: your-feature-name"
4. Push your branch:
git push origin feature/your-feature-name

5. Open a **Pull Request** describing your update  

---

## 📬 Contact

**Akanksha Chougule**  
📧 Email: akanksha@example.com  
🔗 GitHub: https://github.com/Akanksh0301

---
