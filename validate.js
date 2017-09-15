var lastFocus;
var testerName;
var testerNameValid;
var testerNameField;
var testStartTimeFieldName;
var testEndTimeFieldName;
var testID;
var testIDValid;
var testIDFieldName;
var testIDInfo = "";
let file = new XMLHttpRequest();
file.open("GET","test_id_req.html",true);
file.send();
file.onreadystatechange = function() {
    if (file.readyState == 4) {
        testIDInfo = file.responseText;
    }
}

document.getElementById("testID").onfocus = function(event) {
    lastFocus = "testID";
    testID = "";
}
testIDFieldName = document.getElementById("testID");

document.getElementById("testStartTime").onfocus = function(event) {
    if (lastFocus != "testStartTime") {
        let initialTime = new Date();
        let re = /\(([^\)]+)\)/;
        let zone = initialTime.toString().match(re)[1];
        testStartTimeFieldName.value = ""+(initialTime.getMonth()+1)+"/"+initialTime.getDate()+"/"+(1900+initialTime.getYear())+" "+
	((initialTime.getHours() < 10 ? "0" : "") + initialTime.getHours()) + ":" +
	((initialTime.getMinutes() < 10 ? "0" : "") + initialTime.getMinutes()) +
	" " + zone;
    }
    lastFocus = "testStartTime";
}
testStartTimeFieldName = document.getElementById("testStartTime");
document.getElementById("testEndTime").onfocus = function(event) {
    if (lastFocus != "testEndTime") {
        let initialTime = new Date();
        let re = /\(([^\)]+)\)/;
        let zone = initialTime.toString().match(re)[1];
        testEndTimeFieldName.value = ""+(initialTime.getMonth()+1)+"/"+initialTime.getDate()+"/"+(1900+initialTime.getYear())+" "+
	((initialTime.getHours() < 10 ? "0" : "") + initialTime.getHours()) + ":" +
	((initialTime.getMinutes() < 10 ? "0" : "") + initialTime.getMinutes()) +
	" " + zone;
    }
    lastFocus = "testEndTime";
}
testEndTimeFieldName = document.getElementById("testEndTime");
document.getElementById("testData").onfocus = function(event) {
    lastFocus = "testData";
}
//document.getElementById("results").onfocus = function(event) {
//    lastFocus = "results";
//}
document.getElementById("tester").onfocus = function(event) {
    lastFocus = "tester";
    testerName = "";
}
testerNameField = document.getElementById("tester");

document.getElementById("testID").onkeyup = function(event) {
    if (lastFocus === "testID") {
        let testID = testIDFieldName.value;
        if (testIDInfo.indexOf(testID) >= 0) {
            testIDNameValid = true;
	    testIDFieldName.removeAttribute("style");
	} else {
	    testIDNameValid = false;
            testIDFieldName.setAttribute("style","color:red");
        }
    }
}
document.getElementById("testStartTime").onkeyup = function(event) {
    lastFocus = "testStartTime";
}
document.getElementById("testEndTime").onkeyup = function(event) {
    lastFocus = "testEndTime";
}
document.getElementById("testData").onkeyup = function(event) {
    lastFocus = "testData";
}
//document.getElementById("results").onkeyup = function(event) {
//    lastFocus = "results";
//}
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
}
