from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

station_ids = ["E70239", "E74439", "E73839"]  # Replace with actual station IDs

def handle_error(error_message):
    """Centralized error handling function."""
    return render_template("error.html", error_message=error_message)

@app.route("/")
def home():
    return render_template("index.html", station_ids=station_ids)

@app.route("/get_tidal_data", methods=["POST"])
def get_tidal_data():
    station_id = request.form.get("station_id")  # Check for both drop-down and custom input
    if not station_id:
        station_id = request.form.get("custom_station_id")

    if station_id:
        root_url = "http://environment.data.gov.uk/flood-monitoring"
        endpoint = f"/id/stations/{station_id}"
        url = root_url + endpoint

        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                value = data["items"]["measures"]["latestReading"]["value"]
                return render_template("result.html", value=value)
            except json.JSONDecodeError as e:
                return handle_error("Error decoding JSON response.")
        else:
            return handle_error(f"Error fetching data: {response.status_code}")
    else:
        return handle_error("Please specify a station ID.")

if __name__ == "__main__":
    app.run(debug=True)
