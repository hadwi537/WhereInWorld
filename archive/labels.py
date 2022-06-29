import geopandas
import matplotlib.pyplot as plt
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

ax = cities.plot()
print(cities)

for x, y, label in zip(cities.geometry.x, cities.geometry.y, cities.name):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

plt.show()