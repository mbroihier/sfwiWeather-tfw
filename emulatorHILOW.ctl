HILOW-0000
testDbID
Test category setup
HILOW-0000
testDbObjective
None
This test case is used only to setup the initial state of the weather server.  It defaults to always pass.
HILOW-0000
forecast
forecast template {"emulatorTime" : "2020-01-20T00:00:00-10:00", "fileName" : "hourly.HILOW-0000", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 10, "windSpeed" : 10, "windDirection" : "E", "shortForecast" : "Wet"} ]}}/Increment temperature 1/Increment wind 1/Total periods 168
HILOW-0000
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}} ] }
HILOW-0000
setup
HILOW-0010
testDbID
Ever increasing wind and temperature
HILOW-0010
testDbObjective
None
With ever increasing windspeed and tempertures, show that the temperature graph and ranges over the week are increasing as expected.
HILOW-0010
forecast
forecast template {"emulatorTime" : "2020-01-21T01:00:00-10:00", "fileName" : "hourly.HILOW-0010", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 10, "windSpeed" : 10, "windDirection" : "E", "shortForecast" : "Wet"} ]}}/Increment temperature 1/Increment wind 1/Total periods 168
HILOW-0010
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}} ] }
HILOW-0010
test
HILOW-0020
testDbID
Ever decreasing wind and temperature
HILOW-0020
testDbObjective
None
With ever decreasing windspeed and tempertures, show that the temperature graph and ranges over the week are decreasing as expected.
HILOW-0020
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0020", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 100, "windSpeed" : 178, "windDirection" : "W", "shortForecast" : "Dry"} ]}}/Increment temperature -1/Increment wind -1/Total periods 168
HILOW-0020
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0020
test
HILOW-0030
testDbID
Temperature exceeds range of temperature - high
HILOW-0030
testDbObjective
None
Given an API forecast reply that has a temperature that is too hot, illustrate that the prior forecast is unaltered.
HILOW-0030
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0030", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 200, "windSpeed" : 0, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0030
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0030
test
HILOW-0040
testDbID
Temperature exceeds range of temperature - low
HILOW-0040
testDbObjective
None
Given an API forecast reply that has a temperature that is too cold, illustrate that the prior forecast is unaltered.
HILOW-0040
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0040", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : -200, "windSpeed" : 0, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0040
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0040
test
HILOW-0050
testDbID
Wind speed is negative
HILOW-0050
testDbObjective
None
Given an API forecast reply that has a unreasonable windspeed, illustrate that the prior forecast is unaltered.
HILOW-0050
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0050", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 72, "windSpeed" : -1, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0050
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0050
test
HILOW-0060
testDbID
Wind speed is too fast
HILOW-0060
testDbObjective
None
Given an API forecast reply that has a negative windspeed, illustrate that the prior forecast is unaltered.
HILOW-0060
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0060", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 72, "windSpeed" : 300, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0060
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0060
test
HILOW-0070
testDbID
Wind speed and temperature are just within tolerance - high side
HILOW-0070
testDbObjective
None
Given an API forecast reply that has a windspeed and temperature just within tolerance, illustrate that the forecast is updated.
HILOW-0070
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0070", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : 199, "windSpeed" : 299, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0070
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0070
test
HILOW-0080
testDbID
Wind speed and temperature are just within tolerance - low side
HILOW-0080
testDbObjective
None
Given an API forecast reply that has a windspeed and temperature just within tolerance, illustrate that the forecast is updated.
HILOW-0080
forecast
forecast template {"emulatorTime" : "2020-01-21T02:00:00-10:00", "fileName" : "hourly.HILOW-0080", "properties" : {"periods" : [ {"number" : 1, "startTime" : "2020-01-20T00:00:00-10:00", "temperature" : -199, "windSpeed" : 0, "windDirection" : "W", "shortForecast" : "something else"} ]}}/Increment temperature 0/Increment wind 0/Total periods 168
HILOW-0080
alerts
alerts template {"features" : [ { "properties" : {"headline" : "end of the world"}},{"properties" : {"headline" : "big bang"}}] }
HILOW-0080
test
