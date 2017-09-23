document.onmousedown = function(event) {
  console.log("key is up: " + event);
  console.log(event.explicitOriginalTarget.name);
  console.log(event.explicitOriginalTarget.checked);
}
