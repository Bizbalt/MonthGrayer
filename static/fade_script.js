//toggle var
var fade_state = true;
//on btn click
function fade() {
  //get the button and div
  let div = document.getElementById("div");
  let btn = document.getElementById("fade");
  //if faded in or out
  if (fade_state === true) {
    //triggers animation
    div.style.animation = "fade-out 2s forwards";
    //sets the text
    btn.innerHTML = "fade-in";
    //sets fade_state
    fade_state = false;
  } else if (fade_state === false) {
    //triggers animation
    div.style.animation = "fade-in 2s forwards";
    //sets the text
    btn.innerHTML = "fade-out";
    //sets fade_state
    fade_state = true;
  }
}
function auto_fade_in(container) {
  //triggers animation
  container.style.animation = "fade-in 1s forwards";
}

function auto_fade_out(container) {
  //triggers animation
  container.style.animation = "fade-out 1s forwards";
}