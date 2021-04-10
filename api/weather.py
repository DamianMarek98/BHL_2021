import json
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel

import requests

import helper

app = FastAPI()


class Weather(BaseModel):
    time: str = None
    temp_c: float = None
    wind_kph: float = None
    cloud: int = None
    condition_icon: Optional[str] = None


@app.get("/current", response_model=Weather)
async def get_current_weather():
    return Forecast().get_current_weather()


@app.get("/forecast", response_model=List[Weather])
async def get_weather_forecast():
    return Forecast().get_weather_forecast()


class Forecast():
    endpoint: str = "http://api.weatherapi.com/v1/"
    forecast_url: str = "forecast.json"
    current_url: str = "current.json"
    key: str = "679b066563a0457381e164558210904"
    days: int = 3
    city: str = "Gdansk"
    payload = {}
    headers = {}

    def get_current_weather(self) -> Weather:
        params: dict = {"key": self.key, "q": self.city}
        url: str = helper.ApiHelper().prepare_url(self.endpoint + self.current_url, params)
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        current_dict = json.loads(response.text)
        current = current_dict['current']
        weather = Weather()
        weather.time = current['last_updated']
        weather.temp_c = current['temp_c']
        weather.wind_kph = current['wind_kph']
        weather.cloud = current['cloud']
        condition = current['condition']
        weather.condition_icon = condition['icon']
        return weather

    def get_weather_forecast(self) -> list:
        params: dict = {"key": self.key, "q": self.city, "days": str(self.days)}
        url: str = helper.ApiHelper().prepare_url(self.endpoint + self.forecast_url, params)
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        return self.get_list_from_forecast(response.text)

    def get_list_from_forecast(self, weather):
        forecast_dict = json.loads(weather)
        forecast_days = forecast_dict['forecast']
        forecasts = []
        for forecast_day in forecast_days['forecastday']:
            for hour in forecast_day['hour']:
                weather = Weather()
                weather.time = hour['time']
                weather.temp_c = hour['temp_c']
                weather.wind_kph = hour['wind_kph']
                weather.cloud = hour['cloud']
                forecasts.append(weather)

        return forecasts

