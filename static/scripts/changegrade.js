// get the relevant elements
let changeMark = document.forms[0]['changed_mark'];
let mark_msg = document.getElementById("mark_msg");
let form = document.forms[0];

// if a grade change was successfully submitted, send an alert
window.onload = function () {
    if (document.getElementById("hidden").innerHTML.trim() == "success") {
        setTimeout( function() {alert("Mark has been updated");}, 100);
    }
}

// validate to check if form is empty
form.onsubmit = function () {
    return validate();
}

function validate () {
    // check if the uid or the mark chang fields are empty
    if (changeMark.value == "") {
        // provide error message if empty
        mark_msg.innerHTML = "Please enter a new mark"
        mark_msg.style.color = "red";
        changeMark.style.border = "1px solid red";
        return false;
    }
    // if both fields are not empty then ok to submit
    return true;
}
