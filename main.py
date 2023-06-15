from flask import Flask, render_template
import folium

latitude = 48.13720
longitude = 11.51000

app = Flask(__name__)

@app.route("/")
def render_main_page():
    return render_template("index.html")

@app.route("/geo")
def base():

    map = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        tiles="Stamen Terrain"
        )
    
    folium.Marker(
        location=[latitude, longitude],
        popup="<b>Dein Standord!</b>",
        tooltip="Klicke, um mehr zu erfahren!",
        icon=folium.Icon(color="red"),
    ).add_to(map)

    return map._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)