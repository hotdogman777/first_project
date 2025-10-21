import folium
from folium import FeatureGroup


class RainMap:
    def __init__(self, yearly_avg_df, location_data):
        self.df = yearly_avg_df
        self.location_data = location_data

    def create_layer(self):
        rain_layer = FeatureGroup(name="🌧️ 강우량")

        for _, row in self.df.iterrows():
            name = row["지점명"]
            if name in self.location_data:
                lat, lon = self.location_data[name]
                rain = round(row["강수량(mm)"], 2)
                popup_html = f"""
                <div style="font-size:14px; text-align:center; white-space:nowrap;">
                <b>{name}</b> 🌧️ 강우량: {rain} mm
                </div>
                """
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=rain * 0.3,
                    color="blue",
                    fill=True,
                    fill_color="blue",
                    fill_opacity=0.5,
                    popup=popup_html,
                    max_width=250
                ).add_to(rain_layer)

        return rain_layer
