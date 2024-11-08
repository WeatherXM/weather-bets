import h3
import geopandas as gpd
from shapely.geometry import Polygon,shape
import matplotlib.pyplot as plt
import contextily as ctx
import os
from dotenv import load_dotenv
import json
load_dotenv()

GEOJSON_URL = os.getenv('GEOJSON_URL')  

def get_outer_boundary(url):
    print(url)
    gdf = gpd.read_file(url)
    london_bd = gdf.dissolve()
    boundary_coords = list(london_bd.geometry.iloc[0].exterior.coords)
    polygon = Polygon(boundary_coords)
    with open('geojson/boundary_coords.json', 'w') as file:
        json.dump(polygon.__geo_interface__, file)
    return polygon

def initialize_london_boundary():
    polygon = get_outer_boundary(GEOJSON_URL)
    return polygon

def get_cells_from_polygon(polygon, resolution):
    exterior_coords = [[coord[1], coord[0]] for coord in polygon.exterior.coords]
    geojson_polygon = {
        "type": "Polygon",
        "coordinates": [exterior_coords]
    }
    h3_cells = h3.polyfill(geojson_polygon, resolution)
    return h3_cells

def visualize_h3_cells_on_map(h3_cells, london_boundary):
    h3_polygons = [Polygon(h3.h3_to_geo_boundary(h3_cell, geo_json=True)) for h3_cell in h3_cells]
    h3_gdf = gpd.GeoDataFrame(geometry=h3_polygons, crs="EPSG:4326")
    london_gdf = gpd.GeoDataFrame(geometry=[london_boundary], crs="EPSG:4326")
    h3_gdf = h3_gdf.to_crs(epsg=3857)
    london_gdf = london_gdf.to_crs(epsg=3857)
    ax = london_gdf.plot(figsize=(10, 10), edgecolor='black', facecolor='none')
    h3_gdf.plot(ax=ax, alpha=0.6, edgecolor='blue')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.savefig("geojson/london_h3_plot.png")
    plt.close()

resolution = 7

def plt_london():
    with open('geojson/boundary_coords.json', 'r') as file:
        geojson_data = json.load(file)
    boundary = shape(geojson_data)
    london_h3_cells = get_cells_from_polygon(boundary, resolution)
    visualize_h3_cells_on_map(london_h3_cells, boundary)

def geo_filter(df):
    #london_boundary = get_outer_boundary(GEOJSON_URL)
    with open('geojson/boundary_coords.json', 'r') as file:
        geojson_data = json.load(file)
    # Convert GeoJSON to a Polygon object
    boundary = shape(geojson_data)
    london_h3_cells = get_cells_from_polygon(boundary, resolution)
    return df.loc[df['cell_id'].isin(london_h3_cells)]