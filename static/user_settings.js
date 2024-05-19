// ToDo: This file is going to contain the functions to the calls for creating a user, and changing their groups and other settings.
// ToDo: modify existing groups
let current_username = "";
function goto_user_page(username) {
    location.href = "/settings/" + username
}

async function update_user_groups(group){
    let success
    success = await (await fetch(`/user_group_update/${current_username}/${group}`)).text() === "True"
    if (success==="") {
        console.log("Failed to update user group")
    }
    else{
    //    ToDo: log the change with a popup e.g. "add user Gruppenname1
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

    // create new group option
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
    await update_user_groups(group_name)
    // refresh at the end
    goto_user_page(current_username)
}
