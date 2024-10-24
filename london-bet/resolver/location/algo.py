import h3
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import contextily as ctx
import requests

with open('geojson/boundary_coords.txt', 'r') as file:
    london_boundary = file.read()

def get_outer_boundary(url):
    gdf = gpd.read_file(url)
    london_bd = gdf.dissolve()
    boundary_coords = list(london_bd.geometry.iloc[0].exterior.coords)
    with open('geojson/boundary_coords.txt', 'w') as file:
        file.write(f"Polygon({boundary_coords})")
    return Polygon(boundary_coords)

def initialize_london_boundary():
    url = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAC_Dec_2018_Boundaries_EN_BFE_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    polygon = get_outer_boundary(url)
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
    london_h3_cells = get_cells_from_polygon(london_boundary, resolution)
    visualize_h3_cells_on_map(london_h3_cells, london_boundary)

def geo_filter(df):
    london_h3_cells = get_cells_from_polygon(london_boundary, resolution)
    return df.loc[df['cell_id'].isin(london_h3_cells)]