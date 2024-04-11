let current_user = "" // global variable to refrain from loading the same user again
let create_user_opportunity = -1
async function check_user() {
    let btn = document.getElementById("create_user");
    create_user_opportunity = -1
    const user = document.getElementById("current_user").value
    if (user === current_user) { // refrain from loading the same user again
        btn.style.display = "none";
        return
    }
    if (user === "") { // catch empty input
        auto_fade_out(document.getElementById("calendarContainer"))
        return
    }
    const response = await fetch(url + `/user/${user}`)

    const responseText = await response.text()
    btn.innerHTML = "Create new user " + user + "?";
    // fade in calendarContainer if user is not none
    if (responseText === "no user found" || responseText === "") {
        auto_fade_out(document.getElementById("calendarContainer"))
        if (responseText === "no user found") {
            current_user = ""
            create_user_opportunity = 3
            offer_new_user(user)
        }
    }
    else {
        btn.style.display = "none";
        current_user = user
        fillTable()
        //  ToDo: compute the view and then fade in
        // auto_fade_in(document.getElementById("calendarContainer"))
    }
}

async function offer_new_user() {
    while (create_user_opportunity > 0) {
        create_user_opportunity -= 1
        await new Promise(r => setTimeout(r, 1000))
        if (create_user_opportunity === 0) {
            let btn = document.getElementById("create_user");
            btn.style.display = "inline";
        }
    }
}