// to get width of the input, create a new span element and measure its width
function getWidthOfInput(event) {
    input = document.getElementById("current_user")
    compStyle = window.getComputedStyle(input)
    // generate span
    const tmp = document.createElement("span")
    tmp.style.visibility = "hidden"
    tmp.style.fontFamily = compStyle.fontFamily
    tmp.style.fontSize = compStyle.fontSize
    tmp.style.whiteSpace = "pre"
    tmp.innerText = input.value

    if (event.key.length === 1) { // if visible character
        tmp.innerText = tmp.innerText + event.key
    } else if (event.keyCode === 8) { // if backspace (edge case: backspace on left end)
        tmp.innerText = tmp.innerText.slice(0, -1) // remove last char
    }
    document.body.appendChild(tmp)

    // measure width
    const width = tmp.scrollWidth

    // remove span again
    document.body.removeChild(tmp)

    // add buffer to not look cramped, also minimum width
    return Math.max(width + 40, 300)
}