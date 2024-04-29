const url = this.location.origin + "/"

CELL_STATE = {
    "free": "free",
    "freed": "freed",
    "blocked": "blocked",
    "self_blocked": "self_blocked",
    "past": "past",
}

async function mark_day(td) {
    const classes = td.getAttribute("class")
    const day = td.innerText // day is the distance from the first day of the month.
    let success = false
    switch (classes) {
        case "free":
        case "freed":
            success = await (await fetch(url + `grey_day/${current_user}/${day}`)).text() === "True"
            if (success) {
                td.setAttribute("class", CELL_STATE.self_blocked);
            }
            return;
        case "self_blocked":
            success = await (await fetch(url + `free_day/${current_user}/${day}`)).text() === "True"
            if (success) { // ToDo: If the day was just *recently* self-blocked, it should be set to free instead (e.g. missclick)
                td.setAttribute("class", CELL_STATE.freed);
            }
            return;
        default:
            // ToDo: Flash that td (table data cell) if the action is not allowed
            console.log("Can't mark day " + day)
            return;
    }
}

async function calendarInit() {
    // generate the calendar
    const calendar = document.getElementById("calendar_table")
    const today = new Date()
    const month = today.getMonth() // 0 = Jan, 11 = Dec
    const year = today.getFullYear()
    const weekdayOf1st = new Date(year, month, 1).getDay() // 0 = Sunday, 6 = Saturday
    const emptyFields = (weekdayOf1st - 1) % 7 // 0 = Monday, 6 = Sunday
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    // headline
    const h3 = document.getElementById("month_year")
    h3.innerText = `${months[month]} ${year}`

    // create the header
    let tr = document.createElement("tr")
    calendar.appendChild(tr)
    for (let i = 0; i < 7; i++) {
        let th = document.createElement("th")
        th.innerText = weekdays[i]
        tr.appendChild(th)
    }

    // create the days (empty fields in the beginning to match weekdays)
    for (let i = 0; i < daysInMonth + emptyFields; i++) {
        if (i % 7 === 0) {
            tr = document.createElement("tr")
            calendar.appendChild(tr)
        }
        const td = document.createElement("td")
        tr.appendChild(td)
        if (i < emptyFields) {
            td.innerText = ""
        } else {
            const day = i - emptyFields + 1
            td.innerText = day
            if (day < today.getDate() && month <= today.getMonth() && year <= today.getFullYear()) {
                td.setAttribute("class", CELL_STATE.past)
                td.setAttribute("onclick", "mark_day(this)")
            }
        }


    }
}

// testing generation for multiple months
function currentDayRange(monthRange = 2) { // function gives out a range of dates for a range of months starting from today
    let today = new Date();
    let months = [];
    for (let mon = 0; mon <= monthRange; mon++) {
        let newDate = new Date(today.getFullYear(), today.getMonth() + mon, 1);
        months.push(newDate);
    }
    let dates = [];
    months.forEach(month => {
        let numDays = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
        for (let day = 1; day <= numDays; day++) {
            let newDay = new Date(month.getFullYear(), month.getMonth(), day);
            dates.push(newDay);
        }
    });
    return dates;
}
console.log(currentDayRange().length);

function fillCalendar() {
    //todo: get current free (green) self greyed out (grey) freed again (orange) and greyed out by others (dark_grey) days from user_check.js

    //todo: expects above as array of COLOR
    const days = [CELL_STATE.past, CELL_STATE.past, CELL_STATE.past, CELL_STATE.past, CELL_STATE.past,
    CELL_STATE.past, CELL_STATE.past, CELL_STATE.past, CELL_STATE.blocked, CELL_STATE.blocked,
    CELL_STATE.self_blocked, CELL_STATE.self_blocked, CELL_STATE.free, CELL_STATE.free, CELL_STATE.free,
    CELL_STATE.free, CELL_STATE.blocked, CELL_STATE.blocked, CELL_STATE.blocked, CELL_STATE.blocked,
    CELL_STATE.self_blocked, CELL_STATE.self_blocked, CELL_STATE.free, CELL_STATE.free, CELL_STATE.free,
    CELL_STATE.freed, CELL_STATE.freed, CELL_STATE.freed, CELL_STATE.freed, CELL_STATE.freed, CELL_STATE.freed]

    const calendar = document.getElementById("calendar_table")
    let day = 0
    for (tr of calendar.children) {
        for (td of tr.children) {
            const day = td.innerText
            if (day != null) {
                td.setAttribute("class", days[day - 1]) // -1 because days start at 1, array at 0
            }
        }
    }
}