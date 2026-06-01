Feature: Weather aggregator API
  As an API consumer
  I want to fetch weather and read stored readings

  Scenario: Fetch weather and read stored history
    Given Open-Meteo returns weather for "Timisoara"
    When I request to fetch weather for "Timisoara"
    Then the response status is 201
    And the response temperature is 22.4
    When I request all readings for "Timisoara"
    Then the response status is 200
    And there are 1 readings for "Timisoara"

  Scenario: Unknown city is not found
    Given Open-Meteo has no results for "UnknownCity"
    When I request to fetch weather for "UnknownCity"
    Then the response status is 404
    When I request all readings for "UnknownCity"
    Then the response status is 200
    And there are 0 readings for "UnknownCity"

  Scenario: Open-Meteo unavailable returns service error
    Given Open-Meteo is unavailable
    When I request to fetch weather for "Timisoara"
    Then the response status is 503
    When I request all readings for "Timisoara"
    Then the response status is 200
    And there are 0 readings for "Timisoara"
