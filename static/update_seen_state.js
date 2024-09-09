// script to check if the current user has checked the calendar

window.addEventListener("beforeunload", rid_blur_and_set_seen_state, false);
window.addEventListener("blur", set_seen_state, false);

function rid_blur_and_set_seen_state(event) { // on unload the blur event is triggered in some browsers
    window.removeEventListener("blur", set_seen_state, false);
    set_seen_state(event);
}
function set_seen_state(event) {
    if (auto_fade_state === false) { // if the calendar is visible the user is viable and has seen it
        fetch(`set_seen_state/${current_user}/${event.type}`).then(r => {})//.then(response => response.text());
    }
}
