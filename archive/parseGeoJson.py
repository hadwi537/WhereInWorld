import geopandas
import matplotlib.pyplot as plt
#from sqlalchemy import create_engine


path_to_data = geopandas.datasets.get_path('nybb')
gdf = geopandas.read_file(path_to_data)

print(gdf)

#write to file
#gdf.to_file("my_file.geojson", driver="GeoJSON")


#measure area of each ploygon
gdf = gdf.set_index("BoroName")
gdf["area"] = gdf.area
print(gdf["area"])

#making maps
gdf.plot("area", legend=True)
#gdf.explore("area", legend=False)
plt.show()