from device import NotCompatibleDevice, Device, load_json, save_json


class WeatherStation(Device):
    def __init__(self, device_id: str, device_type: str):
        super().__init__(device_id, device_type)

    def get_name(self) -> str:
        """
        Get the name of the weather station.
        """
        return self.load_device_info().get('name', None)

    def get_brand(self) -> str:
        """
        Get the brand of the weather station.
        """
        return self.load_device_info().get('brand', None)

    def get_model(self) -> str:
        """
        Get the model of the weather station.
        """
        return self.load_device_info().get('model', None)

    def get_temperature(self) -> float:
        """
        Get the current temperature in Celsius.
        """
        return self.load_device_info().get('status', {}).get('temperature_c', None)

    def get_humidity(self) -> float:
        """
        Get the current humidity percentage.
        """
        return self.load_device_info().get('status', {}).get('humidity_percent', None)

    def get_pressure(self) -> float:
        """
        Get the atmospheric pressure in hPa.
        """
        return self.load_device_info().get('status', {}).get('pressure_hpa', None)

    def get_wind_speed(self) -> float:
        """
        Get the current wind speed in km/h.
        """
        return self.load_device_info().get('status', {}).get('wind_speed_kmh', None)

    def get_rainfall(self) -> float:
        """
        Get the rainfall measurement in millimeters.
        """
        return self.load_device_info().get('status', {}).get('rainfall_mm', None)

    def get_location(self) -> str:
        """
        Get the location of the weather station.
        """
        return self.load_device_info().get('location', None)

    def get_last_updated(self) -> str:
        """
        Get the last updated timestamp of the weather station.
        """
        return self.load_device_info().get('last_updated', None)

if __name__ == "__main__":
    weather_station_device = WeatherStation("weatherstation56789", "WeatherStation")
    weather_station_device.connect_to_device()


    print("Name:", weather_station_device.get_name())
    print("Brand:", weather_station_device.get_brand())
    print("Model:", weather_station_device.get_model())
    print("Temperature (C):", weather_station_device.get_temperature())
    print("Humidity (%):", weather_station_device.get_humidity())
    print("Pressure (hPa):", weather_station_device.get_pressure())
    print("Wind Speed (km/h):", weather_station_device.get_wind_speed())
    print("Rainfall (mm):", weather_station_device.get_rainfall())
    print("Location:", weather_station_device.get_location())
    print("Last Updated:", weather_station_device.get_last_updated())

    weather_station_device.turn_on_off("off")
