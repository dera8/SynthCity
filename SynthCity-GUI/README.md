# SynthCityWeb – Urban Scenario WebApp

**SynthCityWeb** is a modular web application for exploring, managing, and simulating synthetic urban scenarios. It is composed of two main components:

- **Backend** (`SynthCityWebServer-main`) – A FastAPI server with PostgreSQL support
- **Frontend** (`SynthCityWeb-main`) – A modern web interface built with Vite (JS/React)

---

## Requirements

- Python ≥ 3.8
- Node.js ≥ 18
- pip (Python package manager)
- npm (Node.js package manager)

---

## Manual Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SynthCityWeb.git
cd SynthCityWeb
```

### 2. Extract the ZIP Archives

```bash
unzip SynthCityWebServer-main.zip
unzip SynthCityWeb-main.zip
```

### 3. Run the Backend

```bash
cd SynthCityWebServer-main
pip install -r requirements.txt
uvicorn main:app --reload
The backend will be available at: http://127.0.0.1:8000
Interactive API docs (Swagger UI): http://127.0.0.1:8000/docs
```

### 4. Run the Frontend

In a new terminal:

```bash
cd SynthCityWeb-main
npm install
npm run dev
```

The frontend will be available at: http://localhost:3000

