# Eshmor GeoJSON Map Viewer

An interactive web application that displays georeferenced items from the Eshmor API on a map.

## Features

- Interactive map with multiple basemap options (OpenStreetMap, Satellite, Terrain, Dark)
- Marker clustering for better performance with large datasets
- Geolocation support
- Responsive design for both desktop and mobile devices
- Image previews in popups
- Full-screen map view

## Project Structure

```
.
├── get_geojson.py    # Python script to fetch and convert data
├── requirements.txt  # Python dependencies
└── site/            # Web application files
    ├── index.html   # Main web interface
    └── data.geojson # Generated GeoJSON data
```

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Generate GeoJSON data:
```bash
./get_geojson.py
```
This will create `site/data.geojson` by default. You can specify a different output location:
```bash
./get_geojson.py -o path/to/output.geojson
```

3. Open `site/index.html` in a web browser

## Usage

- Use the layer control in the top right to switch between different basemaps
- Click on markers to view item details and images
- Use the location button in the bottom right to center the map on your current location
- Zoom controls are available in the top left

## Development

The project consists of two main components:

1. `get_geojson.py` - Python script to fetch and convert data from the Eshmor API
2. `site/index.html` - Web interface using Leaflet.js for map visualization

## License

MIT License
