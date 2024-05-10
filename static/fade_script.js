//toggle var
var fade_state = true;
//on btn click
// ToDo: 🐞 fade status resets when changed within the 1s fade -> fades in and then the display attribute gets set to none.
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

var auto_fade_state = true; // default is faded

function auto_fade_in(container) {
  if (auto_fade_state === true) {
    // display container with 0 opacity
    container.style.display = "block";
    //triggers animation
    container.style.animation = "fade-in 1s forwards";
    auto_fade_state = false;
  }
}

function auto_fade_out(container) {
  if (auto_fade_state === false) {
    //triggers animation
    container.style.animation = "fade-out 1s forwards";
    // hide container after animation
    setTimeout(function () {
      container.style.display = "none";
    }, 1000);
    auto_fade_state = true;
  }
}