![CI](https://github.com/Tofame/Jarvis-Dashboard/actions/workflows/ci.yml/badge.svg)

# JARVIS – Intelligent Dashboard

**JARVIS** is a smart, modular dashboard that aggregates essential real-time information in one convenient place, helping you stay updated effortlessly.

## Features

Currently implemented components:
- 🌦️ **Weather:** Get up-to-date weather information for your chosen locations.
- 📈 **Stocks:** Track stock market prices and trends.
- 💱 **Currencies:** View currency exchange rates.
- ₿ **Cryptocurrency:** Monitor cryptocurrency prices and movements.
- 📝 **Notes Panel:** A personal notes section for quick reminders and organization. Every note can be either persistent (seen on every app launch, or temporary).

## Technologies

- **Language:** Python  
- **Testing:** Unit tests
- **Interface:** GUI with Tkinter
- **Caching:** Local JSON caching (with plans for database integration)
- **SQLite DB:** Local database - SQLite, that currently is used for storing notes.
- **Configuration:** Environment variables and `.env` support
- **CI/CD with GitHub Actions:** Automatic testing of app functionality 

## Installation & Usage

1. Clone the repository:  
   ```bash
   git clone https://https://github.com/Tofame/Jarvis-Dashboard.git
   cd jarvis
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS  
   .venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. (Optional) Set up your .env file for API keys and configuration.
The project uses sites that require personal API keys:
- https://www.weatherapi.com/my/
- https://finnhub.io/

5. .env look:

WEATHER_API_KEY=XXXXXXXXXXXX

FINNHUB_API_KEY=XXXXXXXXXXXX

6. Run the dashboard:
```python -m jarvis.main```

## Testing
Just run:
```python -m unittest discover -s jarvis/tests/unit```

## Preview Image

![Jarvis_Dashboard_Image](https://github.com/user-attachments/assets/3fde64a3-7032-42d1-8aed-2ad34a8e1192)

https://github.com/user-attachments/assets/cd1042c1-16a9-4559-b8e2-750b7227840f



