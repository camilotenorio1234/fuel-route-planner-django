# Fuel Route Planner – Django API

This project implements a Django REST API that calculates an optimal fuel plan for a road trip within the United States.

## Features
- Computes driving routes using a free routing API (OSRM)
- Determines optimal fuel stops based on fuel prices
- Assumes a maximum vehicle range of 500 miles
- Calculates total fuel cost assuming 10 MPG
- Renders an interactive map using Leaflet

## Tech Stack
- Django 5
- Django REST Framework
- OSRM (routing)
- Nominatim (reverse geocoding with caching)
- Leaflet (map visualization)

## API Endpoint

**POST** `/api/route-plan/`

Example payload:
```json
{
  "start_lat": 40.7128,
  "start_lng": -74.0060,
  "finish_lat": 41.8781,
  "finish_lng": -87.6298
}
