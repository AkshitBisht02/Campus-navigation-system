// ---------------- MAP SETUP ----------------
const southWest = L.latLng(30.2660, 77.9930);
const northEast = L.latLng(30.2700, 77.9990);
const bounds = L.latLngBounds(southWest, northEast);

const map = L.map('map', {
    center: [30.267652, 77.995176],
    zoom: 17.5,
    minZoom: 17,
    maxZoom: 18,
    maxBounds: bounds,
    maxBoundsViscosity: 1.0
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);


// ---------------- STATE ----------------
let nodes = {};
let markers = [];
let start = null;
let end = null;
let pathLayer = null;


// ---------------- LOAD BUILDINGS ----------------
fetch("/api/buildings/")
    .then(res => res.json())
    .then(data => {
        data.forEach(b => {
            nodes[b.name] = {
                lat: b.latitude,
                lng: b.longitude
            };
        });
        addMarkers();
    });


// ---------------- MARKERS ----------------
function addMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    for (const name in nodes) {
        const marker = L.marker([
            nodes[name].lat,
            nodes[name].lng
        ])
            .addTo(map)
            .bindPopup(name);

        marker.on("mouseover", function () {
            this.openPopup();
        });

        marker.on("mouseout", function () {
            this.closePopup();
        });


        marker.on("click", () => handleSelection(name, marker));
        markers.push(marker);
    }
}



// ---------------- SELECTION + RESET ----------------
function handleSelection(name, marker) {
    if (pathLayer) resetMap();

    if (!start) {
        start = name;
        marker.setIcon(startIcon());
    } 
    else if (!end && name !== start) {
        end = name;
        marker.setIcon(endIcon());
        getPath();
    }
}


// ---------------- PATH API ----------------
function getPath() {


    fetch(`/api/path?start=${start}&end=${end}`)
        .then(res => res.json())
        .then(data => {
            pathLayer = L.polyline(data.path, {
                color: "blue",
                weight: 5
            }).addTo(map);

            document.getElementById("distance").innerText =
                `Distance: ${data.distance}`;

            document.getElementById("time").innerText =
                `Time: ${data.time}`;
        });
}


// ---------------- RESET ----------------

map.on("click", () => {
    if (pathLayer || start || end) {

        resetMap();
    }
});

function resetMap() {
    map.removeLayer(pathLayer);
    pathLayer = null;
    start = null;
    end = null;

    document.getElementById("distance").innerText = "";
    document.getElementById("time").innerText = "";
    addMarkers();
}


// ---------------- ICONS ----------------
function startIcon() {
    return L.divIcon({
        html: '<div style="background:green;width:12px;height:12px;border-radius:50%"></div>'
    });
}

function endIcon() {
    return L.divIcon({
        html: '<div style="background:red;width:12px;height:12px;border-radius:50%"></div>'
    });
}
