let current_user = ""
let create_user_opportunity = -1
async function check_user() {
    let btn = document.getElementById("create_user");
    let info_text = document.getElementById("create_user_info");
    create_user_opportunity = -1
    const user = document.getElementById("current_user").value.replace(/ /g, "")
    if (user === current_user) { // refrain from loading the same user again (this function is called on keyup by now)
        return
    }
    if (user === "") { // catch empty input
        auto_fade_out(document.getElementById("calendarContainer"))
        btn.style.display = "none";
        info_text.style.display = "none";
        return
    }
    const response = await fetch(url + `/user/${user}`)

    const responseText = await response.text()
    // fade in calendarContainer if user is not none
    if (responseText === "no user found" || responseText === "") {
        auto_fade_out(document.getElementById("calendarContainer"))
        if (responseText === "no user found") {
            // prepare button text for possible incoming user creation prompt
            btn.innerHTML = "Create new user " + user + "?";
            current_user = "" // clear out possible previous different user on same client
            create_user_opportunity = 3 // timer
            await offer_new_user(user)
        }
    }
    else {
        btn.style.display = "none";
        info_text.style.display = "none";
        current_user = user.replace(/ /g, "")
        // change the type of the responseText from string to json
        const markings = JSON.parse(responseText)
        if (fillCalendar(markings)) {
            auto_fade_in(document.getElementById("calendarContainer"))
            document.getElementById("settingsAnchor").href = url + "/settings/" + user
        }
    }
}

async function offer_new_user() {
    while (create_user_opportunity > 0) {
        create_user_opportunity -= 1
        await new Promise(r => setTimeout(r, 1000))
        if (create_user_opportunity === 0) {
            let btn = document.getElementById("create_user");
            btn.style.display = "inline";
            let info_text = document.getElementById("create_user_info");
            info_text.style.display = "block";
            current_user = document.getElementById("current_user").value.replace(/ /g, "")
        }
    }
}