import folium
from folium import FeatureGroup


class SolarMap:
    def __init__(self, yearly_avg_df, location_data):
        self.df = yearly_avg_df
        self.location_data = location_data

    def create_layer(self):
        solar_layer = FeatureGroup(name="☀️ 일사량")

        for _, row in self.df.iterrows():
            name = row["지점명"]
            if name in self.location_data:
                lat, lon = self.location_data[name]
                value = round(row["일사(MJ/m2)"], 2)
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=value * 30,
                    color="orange",
                    fill=True,
                    fill_color="orange",
                    fill_opacity=0.6,
                    popup=f"{name}<br>일사량: {value} MJ/m²"
                ).add_to(solar_layer)

        return solar_layer
