let current_username = "";
const group_options_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
function goto_user_page(username=current_username) {
    location.href = "/settings/" + username
}

async function show_change(change) {
    let dummy_div = document.getElementById("wrapper")
    let infobox = document.createElement("span")
    infobox.setAttribute("class", "info_popup")
    infobox.innerText = change
    dummy_div.appendChild(infobox)
    setTimeout(() => {
        infobox.classList.add("animated")
    }, 100); // Delay for 100ms
    await new Promise(r => setTimeout(r, 1200)) // wait a little bit less than the animation takes
    infobox.remove()
}

async function update_user_groups(group){
    let success
    success = await (await fetch(`/user_group_update/${current_username}/${group}`)).text()
    if (success==="") {
        console.log("Failed to update user group")
    }
    else{
        console.log(success)
        await show_change(success)
        if(success.includes("removed group"))
            goto_user_page()
    }
}

async function settings_init(){
    // population of the group container: 1st existing groups, then create new group option
    const group_container = document.getElementById("groupSettingsContainer")

    const response = await fetch(`/user_group_settings/${current_username}`)
    const responseText = await response.text()
    const groups = JSON.parse(responseText)

    for (const [group, tick] of Object.entries(groups)){
        const checkbox = document.createElement("input")
        checkbox.setAttribute("type", "checkbox")
        checkbox.setAttribute("id", group)
        if (tick === "true"){
            checkbox.setAttribute("checked", "")
        }

        const checkbox_label = document.createElement("label")
        checkbox_label.innerText = group
        checkbox.addEventListener("change", () => {
            update_user_groups(group)
        });

        const group_div = document.createElement("div")
        group_div.setAttribute("class", "group_div")
        group_div.appendChild(checkbox)
        group_div.appendChild(checkbox_label)

        group_container.appendChild(group_div)
    }

    // create new (or manage) group option
    const new_group_checkbox = document.createElement("input")
    new_group_checkbox.setAttribute("type", "checkbox")
    new_group_checkbox.setAttribute("id", "new_group")
    const new_group_label = document.createElement("label")
    new_group_label.innerText = "Create new group"

    const new_group_div = document.createElement("div")
    new_group_div.setAttribute("class", "group_div")
    new_group_div.appendChild(new_group_checkbox)
    new_group_div.appendChild(new_group_label)

    // set a fade div for creating a new group options
    const new_group_fade_div = document.createElement("div")
    new_group_fade_div.setAttribute("class", "fade_div")

    const new_group_name = document.createElement("input")
    new_group_name.setAttribute("type", "text")
    new_group_name.placeholder = "New group name"
    new_group_fade_div.appendChild(new_group_name)

    const create_button = document.createElement("button")
    create_button.innerText = "Create Group"
    create_button.addEventListener("click", () => {
     new_group(new_group_name.value);
    })
    new_group_fade_div.appendChild(create_button)

    // additional tick boxes to create group settings like highlighting holidays/blocking all weekdays etc.
    const header = document.createElement("header")
    header.innerText = "Weekdays blocked by default:"
    header.style.padding = "10px"
    const default_signed_days_div = document.createElement("div")
    default_signed_days_div.style.display = "flex"
    default_signed_days_div.style.justifyContent = "center"

    // I want to align the options beside each other this time
    for (let opt = 0; opt < group_options_list.length; opt++) {
        const group_defaults_div = document.createElement("div")
        const checkbox = document.createElement("input")
        checkbox.setAttribute("type", "checkbox")
        checkbox.setAttribute("id", group_options_list[opt])
        const checkbox_label = document.createElement("label")
        checkbox_label.innerText = group_options_list[opt]
        group_defaults_div.style.padding = ".5rem"
        group_defaults_div.appendChild(checkbox)
        group_defaults_div.appendChild(checkbox_label)

        default_signed_days_div.appendChild(group_defaults_div)
    }
    new_group_fade_div.appendChild(header)
    new_group_fade_div.appendChild(default_signed_days_div)

    // adding webhooks
    const webhook_label = document.createElement("label")
    webhook_label.innerText = "Webhooks:"
    const group_webhooks = document.createElement("input")
    group_webhooks.setAttribute("id","webhooks")
    group_webhooks.setAttribute("type", "text")
    group_webhooks.style.width = "350px"
    group_webhooks.placeholder = "webhooks separated by spaces"
    new_group_fade_div.appendChild(webhook_label)
    new_group_fade_div.appendChild(group_webhooks)

    new_group_checkbox.addEventListener("change", () => {
        if (new_group_checkbox.checked) {
            new_group_name.value = ""
            auto_fade_in(new_group_fade_div)
        } else {
            auto_fade_out(new_group_fade_div)
        }
    });

    group_container.appendChild(new_group_div)
    document.body.appendChild(new_group_fade_div)
}

async function new_group(group_name){
    // create the new group
    await update_user_groups(group_name)

    // set the days blocked by default
    let defaults_list = []
    for (let opt = 0; opt < group_options_list.length; opt++){
        let state = (document.getElementById(group_options_list[opt]).checked)
        if (state){state = 1}
        else {state = 0}
        defaults_list[opt] = state
    }
    // only send request if one or more defaults are set
    const sum = arr => arr.reduce((acc, a) => acc + a, 0)
    if (sum(defaults_list)>0){
        // convert boolean to binary string
        let result = await (await fetch(`/group_defaults/${defaults_list.join("")}/${group_name}`)).text()
        if (result==="") {
            console.log("something went wrong setting the default days")
        }
        else{
            console.log(result)
        await show_change(result)
        }
    }

    let webhooks = document.getElementById("webhooks").value
    // only send request when a Webhook is given
    if (webhooks.length>0){
        let result2 = await fetch(`/group_hooks/${group_name}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"webhooks": webhooks})
        })
        result2 = await result2.text()
        if (result2==="") {
            console.log("something went wrong setting webhooks")
        }
        else{
            console.log(result2)
        }
        await show_change(result2)
    }

    // refresh at the end
    goto_user_page(current_username)
}
