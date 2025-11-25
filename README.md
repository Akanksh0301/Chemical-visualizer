# Chemical Equipment Parameter Visualizer

A **hybrid Web + Desktop application** for visualizing and analyzing chemical equipment parameters. This tool helps users explore, monitor, and interpret chemical datasets through interactive charts, tables, and analytics.

---

## Table of Contents

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

## Features

- Upload and manage chemical datasets.
- Interactive visualizations (charts, graphs, tables) for analysis.
- Multi-platform support (web & desktop).
- Real-time data monitoring.
- Export charts and results for reporting.

---

## Technologies Used

- **Frontend:** React.js, Axios, Recharts, CSS, HTML5
- **Backend:** Django / Flask (customize depending on your backend)
- **Database:** SQLite
- **Build Tools:** Webpack, npm
- **Version Control:** Git & GitHub
- **Desktop:** Electron.js (if packaged as a desktop app)

---

## Installation

### 1. Clone the Repository
git clone https://github.com/Akanksh0301/Chemical-visualizer.git
cd chemical-visualizer

**2. Frontend Setup**
cd chemical-visualizer-frontend
npm install       # Install dependencies
npm start         # Run frontend locally at http://localhost:3000
If you encounter polyfill issues (webpack v5+), install missing modules:
npm install stream-http https-browserify stream-browserify util browserify-zlib url assert

**3. Backend Setup**
cd ../backend
pip install -r requirements.txt  # Install dependencies
python manage.py migrate         # Apply database migrations
python manage.py runserver       # Run backend server
Usage
Open the frontend in your browser (http://localhost:3000).

Navigate to Upload Page to upload your chemical dataset.

Explore your data via History Page or Detail Page.

Visualizations can be exported or saved for reports.

Monitor datasets in real-time if backend supports live updates.

**4.Project Structure**
chemical-visualizer/
├─ backend/                  # Backend code (Django/Flask)
│  ├─ db.sqlite3
│  ├─ media/uploads/
│  └─ ... 
├─ chemical-visualizer-frontend/   # Frontend React app
│  ├─ node_modules/
│  ├─ public/
│  ├─ src/
│  ├─ package.json
│  └─ README.md
├─ backend.zip               # Optional backup (ignored in git)
├─ bfg-1.15.0.jar            # Optional BFG cleanup tool
└─ README.md                 # This file

**Contributing**

We welcome contributions! Steps:
Fork the repository.
Create a feature branch:
git checkout -b feature/your-feature-name

Commit your changes:
git commit -m "Add feature: your-feature-name"

Push the branch:
git push origin feature/your-feature-name
Create a Pull Request and describe your changes.

**Contact**
Akanksha Chougule
Email: akanksha@example.com
GitHub: https://github.com/Akanksh0301


