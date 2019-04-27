let message = document.getElementById("remark_message");
let form = document.getElementsByTagName("form")[0];

window.onload = function() {
    // if student has submitted a remark request already, give a message
    if (message.innerHTML.trim() === "You have already submitted a remark request for this grade") {
        document.getElementsByName("remark_reason")[0].focus();
        message.style.color = "red";
        setTimeout(function() {alert("You have already submitted a remark request for this grade");}, 100);
    }
    // give a message saying remark request submitted
    if (message.innerHTML.trim() === "Remark request submitted") {
        document.getElementsByName("remark_reason")[0].focus();
        message.style.color = "red";
        setTimeout(function() {alert("Remark request submitted");}, 100);
    }
}


// Validate the form on submission to make sure fields aren't empty
form.onsubmit = function () {
    if (document.getElementsByTagName("textarea")[0].value === "") {
        message.innerHTML = "Remark reason is required";
        message.style.color = "red";
        document.getElementsByName("remark_reason")[0].focus();
        return false
    }
}

