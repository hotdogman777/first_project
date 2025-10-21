import folium
from folium import FeatureGroup


class CombinedMap:
    def __init__(self, yearly_avg_df, location_data):
        self.df = yearly_avg_df
        self.location_data = location_data

    def create_layer(self):
        combo_layer = FeatureGroup(name="☀️🌧️ 일사↑ + 강우↓ (교집합)")

        solar_mean = self.df["일사(MJ/m2)"].mean()
        rain_mean = self.df["강수량(mm)"].mean()

        for _, row in self.df.iterrows():
            name = row["지점명"]
            if name in self.location_data:
                lat, lon = self.location_data[name]
                solar = row["일사(MJ/m2)"]
                rain = row["강수량(mm)"]

                if solar > solar_mean and rain < rain_mean:
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=10,
                        color="green",
                        fill=True,
                        fill_color="green",
                        fill_opacity=0.8,
                        popup=f"{name}<br>일사량: {solar:.2f}<br>강우량: {rain:.2f}"
                    ).add_to(combo_layer)

        return combo_layer
