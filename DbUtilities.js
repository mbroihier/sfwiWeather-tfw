// Utility to convert test database format to JSON format
var convertDbToJSON = function(book, callback) {
  let fs = require("fs");
  let readLine = require("readline");
  let dbFiles = [".testDbID",
                 ".testDbResults",
                 ".testDbProcedures",
                 ".testDbPre",
                 ".testDbPost",
                 ".testDbObjective",
                 ".testDbExpectedResults"];
  //'.testDbCategoryTitle',
  //'.testDbCategoryDescription'];

  let sections = [];
  let jsonFullDatabase;
  let bookFile = readLine.createInterface({ input: fs.createReadStream(book)});
  bookFile.on("line", function (line) {
      sections.push(line);
    });
  bookFile.on("close", function(error) {
      let processedSections = 0;
      let sectionBuffers = {};
      for (let section of sections) {
        //asynchronously read all of the database files and convert to a JSON consumable string
        let processedFiles = 0;
        let dbBuffers = {};
        let requirements = "";
        let fileHandles = [];
        console.log("processing: " + section);
        for (let postfix of dbFiles) {
          console.log("file: " + postfix);
          let fullPath = section + postfix;
          let line = "";
          let buffer = "";
          let lineCount = 0;
          let dbFile = readLine.createInterface({ input: fs.createReadStream(fullPath)});
          fileHandles.push(dbFile); // save this file handle until processing is complete
          //JSONize the database
          dbFile.on("line", function (line) {
              if (lineCount === 0) {
                if (line.indexOf(':') >= 0) {
                  requirements += '"' + line.slice(0,line.indexOf(':')) + '" : "' +
                    line.slice(line.indexOf(':') + 1) + '"';
                  line = line.slice(0,line.indexOf(':'));
                }
                //buffer = '{ "' + postfix.slice(1) + '" : { "' + line + '" : "';
                buffer = '"' + postfix.slice(1) + '" : { "' + line + '" : "';
              } else if (lineCount % 2 === 0) {
                if (line.indexOf(':') >= 0) {
                  requirements += ', "' + line.slice(0,line.indexOf(':')) + '" : "' +
                    line.slice(line.indexOf(':') + 1) + '"';
                  line = line.slice(0,line.indexOf(':'));
                }
                buffer += ',  "' + line + '" : "';
              } else {
                for (let i = 0; i < line.length; i++) {
                  if (line[i] == '"') {
                    buffer += '\\' + line[i];
                  } else if (line[i] == '\\') {
                    buffer += '\\' + line[i];
                  } else {
                    buffer += line[i];
                  }
                }
                buffer += '"';
              }
              lineCount++;
            });
          dbFile.on("close", function () {
              console.log("closing file");
              processedFiles++;
              let wasEmpty = false;
              if (buffer.length == 0) {
                console.log("buffer length was zero - process an empty file for postfix: " + postfix);
                dbBuffers[postfix] = '"' + postfix.slice(1) + '" : {}';
                buffer = dbBuffers[postfix];
                wasEmpty = true;
              } else {
                dbBuffers[postfix] = buffer + '}';
              }
              if (processedFiles == dbFiles.length) {
                let fullBuffer = '{ ';
                for (let postfix of dbFiles) {
                  fullBuffer += dbBuffers[postfix] + ',';
                }
                if (wasEmpty) {
                  fullBuffer += buffer + ', \"requirements\" : {' + requirements + '}}'; 
                } else {
                  console.log("shouldn't come through here when db is empty");
                  fullBuffer += buffer + '}, \"requirements\" : {' + requirements + '}}'; 
                }
                fileHandles = []; // dispose of all file handles
                sectionBuffers[section] = fullBuffer;
                processedSections++;
                //console.log(fullBuffer);
                //let jsonFullBuffer = JSON.parse(fullBuffer);
                //console.log(jsonFullBuffer);
              } else {
                if (! wasEmpty) {
                  dbBuffers[postfix] = buffer + '}';
                }
              }
              if (processedSections == sections.length && processedFiles == dbFiles.length) {
                // put sections together and convert the string to a JSON object
                let fullSectionBuffer = "{ ";
                for (let tempSection of sections) {
                  if (tempSection == sections[sections.length - 1]) {
                    fullSectionBuffer += '"' + tempSection + '" : ' + sectionBuffers[tempSection] + " } ";
                  } else {
                    fullSectionBuffer += '"' + tempSection + '": ' + sectionBuffers[tempSection] + " , ";
                  }
                }
                console.log(fullSectionBuffer);
                jsonFullDatabase = JSON.parse(fullSectionBuffer);
                callback(jsonFullDatabase);
                console.log(jsonFullDatabase);
              }

            });
        }
      }
    } );
};
var convertJSONToDb = function (jsonDb, callback) {
  var fs = require("fs");
  //console.log (jsonDb);
  for (let category in jsonDb) {
    console.log(category);
    for (let paragraph in jsonDb[category]) {
      //console.log("   " + paragraph);
      let fileHandle = fs.openSync(category + "." + paragraph, "w");
      for (let paragraphInfo in jsonDb[category][paragraph]) {
        if (paragraph == "testDbObjective") {
          //console.log("      " + paragraphInfo + ": " + jsonDb[category]['requirements'][paragraphInfo]);
          fs.writeSync(fileHandle, paragraphInfo + ":" + jsonDb[category]['requirements'][paragraphInfo] + "\n");
        } else {
          //console.log("      " + paragraphInfo);
          fs.writeSync(fileHandle, paragraphInfo + "\n");
        }
        //console.log("      " + jsonDb[category][paragraph][paragraphInfo]);
        fs.writeSync(fileHandle, jsonDb[category][paragraph][paragraphInfo] + "\n");
      }
      fs.closeSync(fileHandle);
    }
  }
  callback("done");
};

module.exports.convertDbToJSON = convertDbToJSON;
module.exports.convertJSONToDb = convertJSONToDb;
