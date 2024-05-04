const url = this.location.origin + "/"

const CELL_STATE = {
    free: "free",
    freed: "freed",
    blocked: "blocked",
    self_blocked: "self_blocked",
    past: "past",
}

async function mark_day(td) {
    const classes = td.getAttribute("class")
    const distance = td.distance  // day is the distance from the first day of the month.
    let success = false
    switch (classes) {
        case "free":
        case "freed":
            success = await (await fetch(url + `grey_day/${current_user}/${distance}`)).text() === "True"
            if (success) {
                td.setAttribute("class", CELL_STATE.self_blocked);
            }
            return;
        case "self_blocked":
            success = await (await fetch(url + `free_day/${current_user}/${distance}`)).text() === "True"
            if (success) { /* ToDo: If the day was just *recently* self-blocked, it should be set to free instead
            (e.g. missclick) This should e checked over "did all already vote?" process:
            If the last vote from that user was on the same day do not mark it as freed but free */
                td.setAttribute("class", CELL_STATE.freed);
            }
            return;
        default:
            // ToDo: Flash that td (table data cell) if the action is not allowed
            console.log("Can't mark day " + distance)
            return;
    }
}

async function calendarInit(month_range = 2) {
    const calendarContainer = document.getElementById("calendarContainer")
    // generate the calendar
    const today = new Date()
    const month = today.getMonth() // 0 = Jan, 11 = Dec
    const year = today.getFullYear()

    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    // redo the following month creating calendar according to the month range
    for (let m_r = 0; m_r < month_range+1; m_r++) {
        // headline
        let currentMonth = month + m_r
        let currentYear = year
        if (currentMonth > 12){
            currentMonth -= 12
            currentYear = year + 1
        }

        const weekdayOf1st = new Date(currentYear, currentMonth, 1).getDay() // 0 = Sunday, 6 = Saturday
        const emptyFields = (weekdayOf1st - 1) % 7 // 0 = Monday, 6 = Sunday
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()

        const h2 = document.createElement("h2")
        h2.innerText = `${months[currentMonth]} ${year}`
        h2.setAttribute("class", "h2")
        calendarContainer.appendChild(h2)

        // create the table
        const calendar = document.createElement("table")
        calendar.setAttribute("id", "calendar_table")

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
                td.innerText = day.toString()
                td.setAttribute("class", CELL_STATE.past)
                td.setAttribute("onclick", "mark_day(this)")
            }
        }
        calendarContainer.appendChild(calendar)
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

function fillCalendar(markings) {
    // check size of markings against expected sizes
    const markingsLength = currentDayRange().length
    let day_distance = 0
    if (markings.length !== markingsLength) {
        console.log("Error: markings array does not match the expected size, are you in the same time")
        return
    }

    // ToDo: fill multiple months according to range
    const calendarContainer = document.getElementById("calendarContainer")
    // initialize a calendar table list
    const calendarTables = Array()
    let element;
    for (element of calendarContainer.children) {
        if (element.tagName === "TABLE") {
            calendarTables.push(element)
        }
    }
    for (ct of calendarTables) {
        for (tr of ct.children) {
            for (td of tr.children) {
                // check if the inner text is a number
                if (isNaN(td.innerText) || (td.innerText === "")) { // check if the day is not an day element
                    continue
                }
                const day = td.innerText
                const distance = td.distance = day_distance // day is the distance from the first day of the month.
                day_distance++
                console.log("Day: " + day + " Distance: " + distance)
                    td.setAttribute("class", markings[distance]) // -1 because days start at 1, array at 0

            }
        }
    }
    return true // send success for fading in
}