from behave import given, then, when

from tests.service.stubs import (
    stub_city_not_found,
    stub_open_meteo_success,
    stub_open_meteo_unavailable,
)


@given('Open-Meteo returns weather for "{city}"')
def step_open_meteo_returns_weather(context, city):
    stub_open_meteo_success()


@given('Open-Meteo has no results for "{city}"')
def step_open_meteo_no_results(context, city):
    stub_city_not_found()


@given("Open-Meteo is unavailable")
def step_open_meteo_unavailable(context):
    stub_open_meteo_unavailable()


@when('I request to fetch weather for "{city}"')
def step_fetch_weather(context, city):
    context.last_response = context.client.post("/weather/fetch", params={"city": city})


@when('I request all readings for "{city}"')
def step_get_all_readings(context, city):
    context.last_response = context.client.get(f"/weather/{city}")


@then("the response status is {status:d}")
def step_response_status(context, status):
    assert context.last_response is not None
    assert context.last_response.status_code == status


@then("the response temperature is {temperature:g}")
def step_response_temperature(context, temperature):
    assert context.last_response.json()["temperature"] == temperature


@then('there are {count:d} readings for "{city}"')
def step_readings_count(context, count, city):
    readings = context.last_response.json()
    assert len(readings) == count
    if count > 0:
        assert all(item["city"] == city for item in readings)
