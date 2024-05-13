//toggle var
let fade_state = true;
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

let auto_fade_state = true; // default is faded
let revert = false; // if fade in is triggered while fading out

function auto_fade_in(container) {
  if (auto_fade_state === true) {
    // display container with 0 opacity
    container.style.display = "block";
    //triggers animation
    container.style.animation = "fade-in 1s forwards";
    auto_fade_state = false;
  }
  else {
    // if the fade out is still running while fade in is triggered stop the fade out
    revert = true;
  }
}

function auto_fade_out(container) {
  if (auto_fade_state === false) {
    //triggers animation
    container.style.animation = "fade-out 0.3s forwards";
    // hide container after animation
    setTimeout(function () {
      if (revert){
        container.style.display = "block";
        container.style.animation = "fade-in 1s forwards";
        revert = false;
      }
      else{
      container.style.display = "none";
      auto_fade_state = true;
      }
    }, 300);
  }
}