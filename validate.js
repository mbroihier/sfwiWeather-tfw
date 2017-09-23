var lastFocus;
var testerNameValid = false;
var testerNameField;
var testStartTimeFieldName;
var testStartTimeFieldNameValid = false;
var testEndTimeFieldName;
var testEndTimeFieldNameValid = false;
var testIDNameValid = false;
var testIDFieldName;
var testIDInfo = "";

var setSendButtonState = function () {
  if (testerNameValid && testStartTimeFieldNameValid && testEndTimeFieldNameValid && testIDNameValid) {
    document.getElementById("sendButton").removeAttribute("disabled");
  } else {
    document.getElementById("sendButton").setAttribute("disabled", "");
  }
};


let file = new XMLHttpRequest();
file.open("GET","test_id_req.html",true);
file.send();
file.onreadystatechange = function() {
  if (file.readyState == 4) {
    testIDInfo = file.responseText;
  }
};

document.getElementById("testID").onfocus = function(event) {
  lastFocus = "testID";
  testID = "";
};

testIDFieldName = document.getElementById("testID");

document.getElementById("testStartTime").onfocus = function(event) {
  if (lastFocus != "testStartTime") {
    event.preventDefault();
    let initialTime = new Date();
    let re = /\(([^\)]+)\)/;
    let zone = initialTime.toString().match(re)[1];
    testStartTimeFieldName.value = ""+(initialTime.getMonth()+1)+"/"+initialTime.getDate()+"/"+(1900+initialTime.getYear())+" "+
    ((initialTime.getHours() < 10 ? "0" : "") + initialTime.getHours()) + ":" +
    ((initialTime.getMinutes() < 10 ? "0" : "") + initialTime.getMinutes()) +
    " " + zone;
    let timeToTest = new Date(testStartTimeFieldName.value);
    if (timeToTest > new Date()) {
      console.log("error in time calculation" + timeToTest);
    }
  }
  testStartTimeFieldName.removeAttribute("style");
  testStartTimeFieldNameValid = true;
  lastFocus = "testStartTime";
  setSendButtonState();
};

testStartTimeFieldName = document.getElementById("testStartTime");
document.getElementById("testEndTime").onfocus = function(event) {
  if (lastFocus != "testEndTime") {
    event.preventDefault();
    let initialTime = new Date();
    let re = /\(([^\)]+)\)/;
    let zone = initialTime.toString().match(re)[1];
    testEndTimeFieldName.value = ""+(initialTime.getMonth()+1)+"/"+initialTime.getDate()+"/"+(1900+initialTime.getYear())+" "+
    ((initialTime.getHours() < 10 ? "0" : "") + initialTime.getHours()) + ":" +
    ((initialTime.getMinutes() < 10 ? "0" : "") + initialTime.getMinutes()) +
    " " + zone;
  }
  testEndTimeFieldName.removeAttribute("style");
  testEndTimeFieldNameValid = true;
  lastFocus = "testEndTime";
  setSendButtonState();
};
testEndTimeFieldName = document.getElementById("testEndTime");
document.getElementById("testData").onfocus = function(event) {
  lastFocus = "testData";
};

document.getElementById("tester").onfocus = function(event) {
    lastFocus = "tester";
};

testerNameField = document.getElementById("tester");

document.getElementById("testID").onkeyup = function(event) {
  if (lastFocus === "testID") {
    let testID = testIDFieldName.value;
    if (testIDInfo.indexOf(testID) >= 0) {
      testIDNameValid = true;
      testIDFieldName.removeAttribute("style");
      testIDNameValid = true;
    } else {
      testIDNameValid = false;
      testIDFieldName.setAttribute("style","color:red");
    }
  }
  setSendButtonState();
};

document.getElementById("testStartTime").onkeyup = function(event) {
  event.preventDefault();
  let now = new Date();
  let re = /\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2} .+$/;
  if (testStartTimeFieldName.value.match(re)) {
    if (now >= new Date(testStartTimeFieldName.value)) {
      testStartTimeFieldName.removeAttribute("style");
      testStartTimeFieldNameValid = true;
    } else {
      testStartTimeFieldName.setAttribute("style", "color:red");
      testStartTimeFieldNameValid = false;
    }
  } else {
    testStartTimeFieldName.setAttribute("style", "color:red");
    testStartTimeFieldNameValid = false;
  }
  lastFocus = "testStartTime";
  setSendButtonState();
};

document.getElementById("testEndTime").onkeyup = function(event) {
  event.preventDefault();
  let re = /\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2} .+$/;
  if (testEndTimeFieldName.value.match(re)) {
    if (((new Date(testEndTimeFieldName.value) >= new Date(testStartTimeFieldName.value))) && (new Date(testEndTimeFieldName.value) <= new Date())) {
      testEndTimeFieldName.removeAttribute("style");
      testEndTimeFieldNameValid = true;
    } else {
      testEndTimeFieldName.setAttribute("style", "color:red");
      testEndTimeFieldNameValid = false;
    }
  } else {
    testEndTimeFieldName.setAttribute("style", "color:red");
    testEndTimeFieldNameValid = false;
  }
  lastFocus = "testEndTime";
  setSendButtonState();
};

document.getElementById("testData").onkeyup = function(event) {
  lastFocus = "testData";
  setSendButtonState();
};

document.getElementById("tester").onkeyup = function(event) {
  if (lastFocus === "tester") {
    let testerName = testerNameField.value;
    let fields = testerName.split(" ");
    let re = /[A-Z][A-Za-z]*/;
    if (fields.length == 2 && fields[0][0].match(re) && fields[1].length > 0 && fields[1][0].match(re)) {
      testerNameValid = true;
      testerNameField.removeAttribute("style");
    } else {
      testerNameValid = false;
      testerNameField.setAttribute("style","color:red");
    }
    console.log(testerNameValid + " " +testerName);
  }
  setSendButtonState();
};
