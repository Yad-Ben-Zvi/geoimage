#!/usr/bin/env python3

import requests
import json
import sys
import argparse
from typing import Dict, Any
import os

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Fetch data from eshmor.org.il API and convert to GeoJSON format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10000,
        help='Maximum number of results to fetch (default: 10000)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='site/data.geojson',
        help='Output file path (default: site/data.geojson)'
    )
    return parser.parse_args()

def fetch_data(limit: int) -> Dict[str, Any]:
    """Fetch data from the GraphQL API."""
    url = "https://api.eshmor.org.il/graphql"
    
    query = """
    query($size: String) {
        getItems(
            appID: "924c217a-d119-42d3-91af-72ade1e9b2e2"
            index: "objects"
            size: $size
            search: { query: { georeference: "*" } }
        ) {
            total
            items {
                objectId
                titleHE
                image
                georeference {
                    georeference
                }
            }
        }
    }
    """
    
    variables = {
        "size": str(limit)
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables})
    response.raise_for_status()
    return response.json()

def convert_to_geojson(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert the API response to GeoJSON format."""
    features = []
    
    for item in data['data']['getItems']['items']:
        if not item['georeference'] or not item['georeference'][0]['georeference']:
            continue
            
        # Parse the georeference string (format: "[lat,lon]")
        try:
            coords_str = item['georeference'][0]['georeference']
            # Remove brackets and split by comma
            coords = coords_str.strip('[]').split(',')
            lat, lon = map(float, coords)
        except (ValueError, AttributeError, IndexError):
            continue
            
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]  # GeoJSON uses [longitude, latitude]
            },
            "properties": {
                "id": item['objectId'],
                "title": item['titleHE'],
                "image": item['image']
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson

def main():
    args = parse_args()
    
    try:
        data = fetch_data(args.limit)
        geojson = convert_to_geojson(data)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        
        # Write to file
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully wrote {len(geojson['features'])} features to {args.output}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
