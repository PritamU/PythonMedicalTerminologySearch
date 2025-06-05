# 🔍 SNOMED Search API (Dockerized Flask App)

A lightweight Flask application to test and demonstrate different SQL text search techniques (LIKE, ILIKE, regex, FTS,Search Vector, trigram similarity,FTS + Trigram) on a SNOMED medical concepts dataset.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🐳 Run the Project

```bash
docker-compose up --build
```

This will:

- Build the Flask and Postgres services
- Automatically seed the database (if not already seeded) using `seed.py`
- Start the Flask server at: `http://localhost:5000`

---

## 🌱 Seeding Logic

- `seed.py` is responsible for:
  - Creating the database table (if not exists)
  - Checking if records already exist
  - Inserting records from `data.txt` if the table is empty
- It is automatically run inside the container via `entrypoint.sh`.

---

## 🗃️ Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── extensions.py
│   ├── searchLogics.py
│   ├── templates
│       ├── index.html
├── data.txt
├── seed.py
├── run.py
├── entrypoint.sh
├── wait-for-postgres.sh
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🔎 Search Modes Supported

- LIKE / ILIKE
- Regex
- Full Text Search (FTS)
- Precomputed `search_vector` column
- Trigram similarity (`pg_trgm`)
- FTS + Trigram

---

## 📦 Notes

- Make sure `entrypoint.sh` is executable (`chmod +x entrypoint.sh`) before building.
- The app uses `pg_isready` to wait for Postgres before starting Flask and seeding.
