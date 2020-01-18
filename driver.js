
// weather display server driver - sends test data to the weather server and verifies results
// Setup all required packages
// Although the next line refers to jslint, it is altering jshint behavior
/*jslint esversion:6 */
/*jslint node:true, maxerr:50  */
'use strict';
var config = require("./config.js");
var express = require("express");
var fs = require("fs");
var jsdom = require("jsdom");
process.env.TZ = config.timeZone;
var WebSocketServer = require("ws").Server;
// Read test case forecast API templete
var hourly = fs.readFileSync("./hourlyTemplate");
// Read test case alert template
var alerts = fs.readFileSync("./alertsTemplate");
var app = express();

var http = require("http");

// initialize global information

var serverUnderTestReady = 0;
var testDataQueryInProgress = false;
var doGet = false;
var READY = 3;

var testDirectory = process.argv[2];

var tests = fs.readFileSync(testDirectory + '/test.ctl', 'UTF-8');
tests = tests.split("\n");
var testCase = "";

var expectedResults = null;
var testDbResults = "";

var lastReadForecast = "";
var lastReadAlerts = "";
var lastReadExpectedResults = "";

var walkObjectAndTest = function (objectOne, objectTwo, state) {
    for (let property in objectOne) {
        //console.log("looking at", property);
        if (property in objectTwo) {
            if (typeof objectOne[property] == 'object') {
                state = walkObjectAndTest(objectOne[property], objectTwo[property], state);
            } else {
                if (typeof objectOne[property] == 'string') {
                    if (objectOne[property] != objectTwo[property]) {
                        console.log(property, " --> ", objectOne[property], "does not match", objectTwo[property]);
                        console.log("Last Read Forecast:", lastReadForecast);
                        console.log("Last Read Alerts:", lastReadAlerts);
                        console.log("Last Read Expected Results:", lastReadExpectedResults);
                        state = false;
                        break;
                    }
                } else {
                    console.log("Don't know how to handle", typeof objectOne[property]);
                }
            }
        } else {
            console.log("Property", property, "is not in other object");
            state = false;
            break;
        }
    }
    return state;
}

// check for changes 
setInterval(function(){
    let done = false;
    if ((! doGet) && (serverUnderTestReady == READY)) { //server has contacted the driver enough times (gridpoint & alerts requests)
        console.log(tests);
        if (tests.length > 0) {
            testCase = tests.shift();
            done = (testCase == '');
        } else {
            done = true;
        }
        if (done) {
            if (! testDataQueryInProgress) {
                console.log('Test cases for ' + testDirectory + ' finished');
                fs.writeFileSync(testDirectory + '.testDbResults', testDbResults);
                process.exit(0);
            } else {
                console.log ("Delaying exit for check of last test case results");
            }
        } else {
            if (! testDataQueryInProgress) {
                alerts = fs.readFileSync(testDirectory+'/alerts.'+testCase);
                lastReadAlerts = testDirectory+'/alerts.'+testCase;
                hourly = fs.readFileSync(testDirectory+'/hourly.'+testCase);
                lastReadForecast = testDirectory+'/hourly.'+testCase;
                expectedResults = fs.readFileSync(testDirectory+'/expectedResults.'+testCase, 'UTF-8');
                lastReadExpectedResults = testDirectory+'/expectedResults.'+testCase;
                serverUnderTestReady = 0;
                doGet = true;
            }
        }
    }
    if (doGet && (serverUnderTestReady == READY) && (! testDataQueryInProgress)) {
        testDataQueryInProgress = true;
        console.log("Requesting server's internal state");
        let query = http.request({protocol: "http:", hostname: config.forecastURL, path: "/testData", port: 3000, method: "GET"}, function (result) {
            let bodySegments = [];
            //serverUnderTestReady = 0;
            result.on("data", function(data) {
                bodySegments.push(data);
            });
            result.on("end", function() {
                let body = Buffer.concat(bodySegments);
                let replyDOM = new jsdom.JSDOM(body);
                let replyDocument = replyDOM.window.document;
                let serverObject = JSON.parse(replyDocument.body.textContent);
                let expectedResultsObject = JSON.parse(expectedResults);
                //console.log("serverObject: ", serverObject);
                //console.log("expectedResultsObject:", expectedResultsObject);
                let status = walkObjectAndTest(expectedResultsObject, serverObject, true);
                if (status) {
                    console.log(testCase);
                    console.log('PASSED');
                    testDbResults += testCase + '\nPASSED\n';
                } else {
                    console.log(testCase);
                    console.log('FAILED');
                    testDbResults += testCase + '\nFAILED\n';
                    for (let key in expectedResultsObject) {
                        console.log("Contents expectedResultsObject:", expectedResultsObject[key]);
                        console.log("Contents serverObject:", serverObject[key]);
                    }
                }
                testDataQueryInProgress = false;
                doGet= false;
                serverUnderTestReady = 0;
            });
        });
        query.on("error", function(error) {
            console.log("data query error: ", error);
            testDataQueryInProgress = false;
            doGet= false;
            serverUnderTestReady = 0;
        });
        query.end();
    }

},1000);
// if the express server is contacted, look at the request and build a response or
// forward the request to the standard server behavior.
app.get("/gridpoints/*", function(request, response, next) {
    console.log("processing", request.method, "forecast request");
    console.log("with URL", request.url);
    console.log("Using last read forecast:", lastReadForecast);
    // this is the main page so return main page built in updateHTML
    response.send(hourly);
    if (serverUnderTestReady == 0) {
        serverUnderTestReady = 1;
    }
});
app.get("/alerts/*", function(request, response, next) {
    console.log("processing", request.method, "alert request");
    console.log(" with URL", request.url);
    console.log("Using last read alerts:", lastReadAlerts);
    // this is the main page so return main page built in updateHTML
    response.send(alerts);
    if (serverUnderTestReady == 1) {
        serverUnderTestReady = 2;
    } else if (serverUnderTestReady == 2) {
        serverUnderTestReady = 3;
    }
});
// post processing section
// default processing section
app.get("*", function(request, response, next) {
    console.log("fell into default get");
    console.log(request.url);
    console.log(request.method);
    next();
  });
app.post("*", function(request, response, next) {
    console.log("fell into default post");
    console.log(request.url);
    console.log(request.method);
    next();
  });
app.use(express.static("./"));
var ws = new WebSocketServer({server: app.listen(process.env.PORT || config.port)});
console.log("driver is listening and ready");
