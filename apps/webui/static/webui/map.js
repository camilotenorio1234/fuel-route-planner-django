const payload = {
    start_lat: 40.7128,
    start_lng: -74.0060,
    finish_lat: 41.8781,
    finish_lng: -87.6298
};

// Inicializa mapa
const map = L.map("map").setView([39.5, -98.35], 4);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
}).addTo(map);

async function loadRoute() {
    try {
        const res = await fetch("/api/route-plan/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            throw new Error(`API error ${res.status}`);
        }

        const data = await res.json();

        // Ruta
        const routeLayer = L.geoJSON(data.route.geometry, {
            style: { color: "#2563eb", weight: 4 }
        }).addTo(map);

        map.fitBounds(routeLayer.getBounds());

        // Fuel stops
        data.fuel_stops.forEach((stop, i) => {
            L.marker([stop.lat, stop.lng])
                .addTo(map)
                .bindPopup(`
                    <strong>Stop ${i + 1}: ${stop.name}</strong><br/>
                    ${stop.city}, ${stop.state}<br/>
                    Price: $${stop.price_per_gallon}/gal<br/>
                    Gallons: ${stop.gallons_to_buy}<br/>
                    Cost: $${stop.cost}
                `);
        });

        document.getElementById("infoBox").innerHTML = `
            <h3>Fuel Route Plan</h3>
            <p><strong>Total distance:</strong> ${data.route.distance_miles} miles</p>
            <p><strong>Total fuel cost:</strong> $${data.total_fuel_cost}</p>
            <p><strong>Stops:</strong> ${data.fuel_stops.length}</p>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById("infoBox").innerHTML =
            "<h3>Error</h3><p>Failed to load route.</p>";
    }
}

loadRoute();
