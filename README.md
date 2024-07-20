# Weather Forecast

This web application allows users to enter the name of a city and receive a weather forecast. The application features auto-completion for city names, tracks the history of city searches for each user, and provides an API to view the number of times each city was searched.

## Technologies Used

- **Backend Framework**: Django
- **API for Weather Data**: OpenWeatherAPI
- **Containerization**: Docker
- **Other Libraries**:
  - `requests` for making API calls
  - `python-dotenv` for environment variable management

## Installation

1. **Clone the Repository**

```
git clone <repository-url>
cd weather_app
```

2. **Build the Docker Containers**

```
docker-compose build
```

3. **Run the Docker Containers**

```
docker-compose up
```

4. **Access the Application**
   Open your web browser and navigate to http://localhost:8000/.

## Running Tests

```
docker-compose exec web python manage.py test
```
