window.onload = function() {
  let inputElements = document.getElementsByTagName("input");
  let stepTextElements = document.getElementsByTagName("textarea");
  let re = /step\d+/;
  let stepsAdded = 0;
  let initialSize = inputElements.length - 1;
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
      if (element.getAttribute("name") == "Add Step") {
    	  element.onclick = function(event) {
    		  event.preventDefault();
    		  stepsAdded++;
    		  console.log("Need to add a step");
    		  this.removeAttribute("checked");
    		  let div = document.createElement("div");
    		  let box = document.createElement("input")
    		  box.setAttribute("type", "checkbox");
    		  box.setAttribute("checked", "");
    		  box.setAttribute("value", "keepStepLine" + (stepsAdded + initialSize));
    		  box.setAttribute("name", "step" + (stepsAdded + initialSize));
    	      box.onclick = function(event) { // note: use closure to preserve the state of textStepElement
    	          console.log("got a click of a checkbox");
    	          console.log("from: " + this.getAttribute("name"));
    	          if (this.hasAttribute("checked")) {
    	            this.removeAttribute("checked");
    	            textArea.setAttribute("style", "text-decoration: line-through; color: red");
    	            console.log("turning off check");
    	          } else {
    	            this.setAttribute("checked", "");
    	            textArea.removeAttribute("style");
    	            console.log("turning on check");
    	          }
    	          console.log("checked: " + this.hasAttribute("checked"));
    	      };
    		  div.appendChild(box);
    		  let textArea = document.createElement("textArea");
    		  textArea.setAttribute("rows", "2");
    		  textArea.setAttribute("cols", "80");
    		  textArea.setAttribute("name", "stepLine" + (stepsAdded + initialSize));
    		  div.appendChild(textArea);
    		  console.log(this.parentNode);
    		  console.log(this.parentNode.parentNode);
    		  this.parentNode.parentNode.insertBefore(div, this.parentNode);
    	  };
      }
    }
  }
};
