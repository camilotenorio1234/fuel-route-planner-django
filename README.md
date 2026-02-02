# Fuel Route Planner — Django REST API & Interactive Map

## Introduction

Fuel Route Planner is a Django-based REST API that computes optimal fuel stops for long-distance road trips within the United States.

Given a start and finish location, the system calculates the driving route, determines cost-effective refueling points based on fuel prices, and returns the total fuel cost assuming a fixed vehicle range and fuel efficiency.

The project also includes a lightweight web UI that visualizes the route and fuel stops on an interactive map.

---

## Description

This API receives start and finish coordinates within the US and returns:

- Driving route geometry
- Optimal fuel stops based on fuel price optimization
- Total fuel cost assuming:
  - Maximum vehicle range: 500 miles
  - Fuel efficiency: 10 miles per gallon

Routing is handled using a free routing API, while fuel prices are sourced from a provided CSV dataset and loaded once at application startup for performance.

---

## Built With

- Python 3.11
- Django 5.1.7
- Django REST Framework 3.15.2
- OSRM (Open Source Routing Machine)
- Nominatim (OpenStreetMap reverse geocoding)
- Leaflet (map visualization)
- CSV-based fuel price dataset

---

## Project Structure

```sh
fuel_route_planner/
├── apps/
│   ├── fuels/        # CSV loading and fuel price indexing
│   ├── routing/      # Routing logic and fuel optimization
│   ├── webui/        # Lightweight frontend (Leaflet map)
├── config/           # Django project configuration
├── data/
│   ├── fuel-prices-for-be-assessment.csv
│   └── geocode_cache.json
├── manage.py
├── requirements.txt
```
##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/camilotenorio1234/fuel-route-planner-django.git
cd fuel-route-planner-django
```

### 2. Create Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python manage.py runserver
```
The API will be available at:
```sh
http://127.0.0.1:8000/
```

## API Endpoint
### POST /api/route-plan/

**Request Body**

```json
{
  "start_lat": 40.7128,
  "start_lng": -74.0060,
  "finish_lat": 41.8781,
  "finish_lng": -87.6298
}
```

## Response Includes

- route.distance_miles
- route.geometry (GeoJSON LineString)
- fuel_stops (optimized fuel stops)
- total_fuel_cost

## API Testing
The API can be tested using Postman or any HTTP client.

- Send a POST request to /api/route-plan/
- Provide coordinates in JSON format
- The response is deterministic and optimized
- Only one routing API call is performed per request

## Web UI
### Interactive Map

Visit:

```sh
/map/
```


The web interface:
- Consumes the same API endpoint
- Renders the route using Leaflet
- Displays fuel stops as markers
- Shows total distance and total fuel cost

## Requirements

```sh
Django==5.1.7
djangorestframework==3.15.2
requests==2.32.5
asgiref==3.8.1
sqlparse==0.5.3
tzdata==2025.1

```
## Author

**Juan Camilo Muñoz
Django Backend Developer**
