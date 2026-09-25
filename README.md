# 🌦️ Weather Data Pipeline

A Python-based **ETL (Extract, Transform, Load) pipeline** that extracts hourly historical weather data from the **Open-Meteo Historical Weather API** for 10 selected Indian cities, cleans and validates the data, and loads it into an **online Supabase PostgreSQL Database**.

---

## 📑 Contents

- [🌦️ Project Overview](#-project-overview)
- [🏙️ Cities Covered](#️-cities-covered)
- [🔄 Pipeline Architecture](#-pipeline-architecture)
- [🌡️ Weather Variables](#️-weather-variables)
- [🛠️ Tools & Technologies](#️-tools--technologies)
- [📁 Project Structure](#-project-structure)
- [🗄️ Database Design](#️-database-design)
- [⚙️ Project Setup](#️-project-setup)
- [🗄️ Supabase PostgreSQL Setup](#️-supabase-postgresql-setup)
- [▶️ Run the Pipeline](#️-run-the-pipeline)
- [📅 Daily Data Logic](#-daily-data-logic)
- [✅ Data Validation](#-data-validation)
- [📝 Logging](#-logging)
- [🤖 Windows Automation](#-windows-automation)
- [🛑 Fail-Fast Strategy](#-fail-fast-strategy)
- [🔐 GitHub & Security Notes](#-github--security-notes)
- [🚀 Future Improvements](#-future-improvements)
- [📡 Data Source](#-data-source)
- [👤 Author](#-author)

---

## 🌦️ Project Overview

This project demonstrates an end-to-end weather data pipeline using Python.

The pipeline:

1. Gets city coordinates and timezone from the Open-Meteo Geocoding API.
2. Extracts hourly historical weather data from the Open-Meteo Historical Weather API.
3. Adds a `city_id` to identify each city.
4. Cleans and validates the extracted data using Pandas.
5. Loads the cleaned data into an **online Supabase PostgreSQL database on the Free Tier**.
6. Records pipeline activity and errors using Python logging.
7. Can run automatically every day using Windows Task Scheduler.

---

## 🏙️ Cities Covered

The current version extracts hourly weather data for:

```python
city_list = [
    'Kolkata', 'Delhi', 'Mumbai', 'Bengaluru',
    'Pune', 'Surat', 'Chennai', 'Ahmedabad',
    'Hyderabad', 'Jaipur'
]
```

> **Note:** These are the 10 cities currently configured in the project. The city source can be expanded later without changing the overall pipeline architecture.

---

## 🔄 Pipeline Architecture

```text
                    ┌──────────────────────┐
                    │      City List       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Open-Meteo Geocoding │
                    │        API           │
                    └──────────┬───────────┘
                               │
                    Latitude / Longitude
                         / Timezone
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Historical Weather   │
                    │      API             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Extract        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Transform & Validate │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Supabase PostgreSQL  │
                    │      Free Tier      │
                    └──────────────────────┘
```

---

## 🌡️ Weather Variables

The pipeline extracts the following hourly variables:

| Variable | Description |
|---|---|
| `temperature_2m` | Temperature at 2 metres above ground |
| `apparent_temperature` | Feels-like temperature |
| `relative_humidity_2m` | Relative humidity at 2 metres above ground |
| `precipitation` | Precipitation |
| `pressure_msl` | Mean sea-level pressure |
| `cloud_cover` | Cloud coverage |
| `wind_speed_10m` | Wind speed at 10 metres above ground |
| `wind_direction_10m` | Wind direction at 10 metres above ground |
| `weather_code` | WMO weather condition code  |

---

## 🛠️ Tools & Technologies

| Technology | Purpose |
|---|---|
| 🐍 Python | Pipeline development |
| 🌐 Requests | API requests |
| 🐼 Pandas | Data transformation and validation |
| 🐘 PostgreSQL | Relational database |
| ☁️ Supabase | Online PostgreSQL hosting |
| 🆓 Supabase Free Tier | Database hosting for this project |
| 📜 SQL | Database schema and queries |
| 🔐 python-dotenv | Environment variable management |
| 📝 Python Logging | Pipeline monitoring and error logging |
| 🌿 Git | Version control |
| 🐙 GitHub | Source-code hosting & Project Collaboration |
| 🪟 Windows Task Scheduler | Daily automation |

---

## 📁 Project Structure

```text
weather-data-pipeline/
│
├── main.py
├── extract.py
├── transform.py
├── load.py
├── logger_config.py
├── prepare_weather_codes.py
├── weather_data_sql_schema.sql
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── dataset/
│   ├── descriptions.json
│   │
│   ├── raw/
│   │   ├── dim_city.csv
│   │   └── dim_weather.csv
│   │
│   └── processed/
│
└── logs/
```

---

## 🗄️ Database Design

The project uses an **online Supabase PostgreSQL database on the Free Tier**.

The PostgreSQL schema is:

```sql
weather_data
```

### 🏙️ `dim_city`

Stores city metadata:

```text
city_id
city_name
latitude
longitude
country_code
timezone
```

### 🌤️ `dim_weather`

Stores weather-code descriptions:

```text
weather_code
weather_description
```

### 📊 `fact_weather_hourly`

Stores hourly weather measurements:

```text
time
city_id
temperature_2m
apparent_temperature
relative_humidity_2m
precipitation
pressure_msl
cloud_cover
wind_speed_10m
wind_direction_10m
weather_code
```

### 🔗 Relationships

```text
dim_city.city_id
       │
       ▼
fact_weather_hourly.city_id


dim_weather.weather_code
       │
       ▼
fact_weather_hourly.weather_code
```

---

## ⚙️ Project Setup

### 1️⃣ Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd weather-data-pipeline
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

First Rename `.env.example` to `.env` and then add the required environment variables:

Example:

```env
GEOCODING_BASE_URL=https://geocoding-api.open-meteo.com/v1/search
HISTORICAL_WEATHER_BASE_URL=https://archive-api.open-meteo.com/v1/archive

DB_HOST=your-supabase-host
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
```

---

## 🗄️ Supabase PostgreSQL Setup

Before starting the automated pipeline:

### 1️⃣ Create the database tables

Open the Supabase SQL Editor and execute:

```text
weather_data_sql_schema.sql
```

This creates the required PostgreSQL schema and tables.

### 2️⃣ Upload the reference data

Upload these two files into PostgreSQL:

```text
dataset/raw/dim_city.csv
dataset/raw/dim_weather.csv
```

These files provide the initial city and weather-code reference data required by the pipeline.

### 3️⃣ Configure the connection

Copy the required Supabase PostgreSQL connection details into `.env`.

The pipeline then uses these credentials to connect to the online Supabase PostgreSQL database.

---

## ▶️ Run the Pipeline

Run the complete pipeline with:

```bash
python main.py
```

The execution flow is:

```text
Extract
   ↓
Transform
   ↓
Load
```

If a critical step fails, the pipeline logs the error and stops.

---

## 📅 Daily Data Logic

The pipeline dynamically calculates yesterday's date:

```python
start_date = datetime.date.today() - datetime.timedelta(days=1)
```

For example:

```text
Pipeline run date → 2026-09-25
Data extracted    → 2026-09-24
```

Therefore, the same code can run every day without manually changing the date.

---

## ✅ Data Validation

The transformation stage validates the extracted weather data before loading it into PostgreSQL.

Checks include:

- Required columns exist.
- Correct datatypes are present.
- Required values are not null.
- Duplicate `city_id + time` records are detected.
- Weather values are checked against valid ranges.
- Hourly timestamps are checked for missing records.

Invalid or incomplete data stops the pipeline before loading.

---

## 📝 Logging

The project uses Python's built-in `logging` module.

Logs are written to:

```text
logs/pipeline.log
```

The logger records:

- ℹ️ `INFO` — normal pipeline activity
- ⚠️ `WARNING` — unusual but non-critical conditions
- ❌ `ERROR` — operation failure
- 🐞 `EXCEPTION` — error with traceback information

Example:

```text
INFO  | Pipeline Started
INFO  | Successfully extracted data for Kolkata
ERROR | Database connection failed
INFO  | Pipeline Completed Successfully
```

---

## 🤖 Windows Automation

The pipeline can be automated using **Windows Task Scheduler**.

Create:

```text
run_pipeline.bat
```

Example:

```bat
@echo off

cd /d "C:\path\to\weather-data-pipeline"

"C:\path\to\weather-data-pipeline\.venv\Scripts\python.exe" main.py

exit /b %ERRORLEVEL%
```

Then configure Windows Task Scheduler:

```text
Task Scheduler
      ↓
Create Basic Task
      ↓
Trigger: Daily
      ↓
Action: Start a program
      ↓
Program: run_pipeline.bat
```

The PC must be running and connected to the internet when the task executes.

---

## 🛑 Fail-Fast Strategy

The pipeline follows a fail-fast approach:

```text
Extraction
   │
   ├── Failure → Log Error → Stop
   │
   ▼
Transformation
   │
   ├── Failure → Log Error → Stop
   │
   ▼
Loading
   │
   ├── Failure → Log Error → Stop
   │
   ▼
Pipeline Completed Successfully
```

This prevents incomplete daily data from being loaded into PostgreSQL.

---

## 🔐 GitHub & Security Notes

The repository should **not** contain:

```text
.env
.venv/
__pycache__/
*.pyc
logs/
*.log
```

The repository intentionally keeps:

```text
dataset/raw/dim_city.csv
dataset/raw/dim_weather.csv
```

because these are reference files required for the initial PostgreSQL setup.

Daily generated weather CSV files are excluded from GitHub to avoid continuously growing repository size.

---

## 🚀 Future Improvements

- 🌍 Expand the city list beyond the current 10 cities.
- 🗄️ Store city master data directly in PostgreSQL.
- 🔁 Add API retry logic for temporary failures.
- 🛡️ Add stronger duplicate protection during loading.
- 📊 Add automated data-quality reporting.
- 📈 Build a Power BI dashboard connected to PostgreSQL.
- ☁️ Move scheduling from a local PC to a cloud environment.
- ⚡ Process a larger number of cities using batched API requests.

---

## 📡 Data Source

### Open-Meteo

This project uses:

- **Geocoding API** — resolves city names to latitude, longitude, timezone, and location metadata.
- **Historical Weather API** — provides hourly historical weather data.

🔗 [Open-Meteo](https://open-meteo.com/)

### ☁️ Database Hosting

This project uses:

- **Supabase PostgreSQL**
- **Free Tier**
- Online PostgreSQL database for storing the weather pipeline data.

🔗 [Supabase](https://supabase.com/)

---

## 👤 Author

### Biswajit Sasmal

🎓 B.Sc. Mathematics Honours  
💻 Data Analytics & Data Engineering

🔗 **LinkedIn:** [linkedin.com/in/biswajitsasmal](https://www.linkedin.com/in/biswajitsasmal/)  
📧 **Email:** [biswajitsasmal.data@gmail.com](mailto:biswajitsasmal.data@gmail.com)

---