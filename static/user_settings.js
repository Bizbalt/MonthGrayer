// ToDo: This file is going to contain the functions to the calls for creating a user, and changing their groups and other settings.
// ToDo: modify existing groups
let current_username = "";
function create_user(username) {
    location.href = "/settings/" + username
}
async function settings_init(){
    // population of the group container: 1st existing groups, then create new group option
    const group_container = document.getElementById("group_settings_container")

    const response = await fetch(`/user_group_settings/${current_username}`)
    const responseText = await response.text()
    const groups = JSON.parse(responseText)
    const markings = JSON.parse(responseText)
    console.log(markings)
}