window.onload = function() {
  let inputElements = document.getElementsByTagName("input");
  let stepTextElements = document.getElementsByTagName("textarea");
  let re = /step\d+/;
  console.log("Number of input elements found: " + inputElements.length);
  //for (let element of inputElements) { this isn't working on Safari
  for (let index = 0; index < inputElements.length; index++) {
    let element = inputElements[index];
    console.log("processing: " + element + " " + stepTextElements.length);
    let textStepElement;
    if (element.hasAttribute("name")) {
      if (element.getAttribute("name").match(re)) {
        textStepElement = stepTextElements[element.getAttribute("name").replace("step", "stepLine")];
        element.onclick = function(event) { // note: use closure to preserve the state of textStepElement
          console.log("got a click of a checkbox");
          console.log("from: " + this.getAttribute("name"));
          if (this.hasAttribute("checked")) {
            this.removeAttribute("checked");
            textStepElement.setAttribute("style", "text-decoration: line-through; color: red");
            console.log("turning off check");
          } else {
            this.setAttribute("checked", "");
            textStepElement.removeAttribute("style");
            console.log("turning on check");
          }
          console.log("checked: " + this.hasAttribute("checked"));
        };
      }
    }
  }
};
