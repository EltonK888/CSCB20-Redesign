let radio = document.forms['feedback-form']['instructor_uid'];
let feedbackArray = document.getElementsByClassName('questions');
let radioMsg = document.getElementById("instructor_message");
let feedbackMsg = document.getElementById("feedback_message");

// if successfully submitted, then alert the user
window.onload = function () {
    instName = document.getElementById('hidden').innerHTML.trim()
    console.log(instName);
    if (instName !== ''){
        alert("Feedback to " + instName + ' has been submitted')
    }
}

// validate the form on submission
document.getElementById('feedback-form').onsubmit = function () {
    return validate();
}

// validate if the fields of the form are not empty
function validate() {
    // if one of the fields are empty
    if (radio.value === "") {
        // give appropriate error message
        radioMsg.innerHTML = "Please select an instructor";
        radioMsg.style.color = "red";
    } else {
        radioMsg.innerHTML = "";
    }
    // check if the instructor field is empty
    let i;
    let emptyIndexArray = [];
    for (i=0; i<feedbackArray.length; i++) {
        // check if at least one of the fields have been filled
        if (feedbackArray[i].value !== "" && radio.value !== "") {
            return true;
        } else if (feedbackArray[i].value == "") {
            emptyIndexArray.push(i);
        }
    }
    console.log(emptyIndexArray);
    if (emptyIndexArray.length === feedbackArray.length) {
        feedbackMsg.innerHTML = "You must leave feedback for at least one of the fields";
        feedbackMsg.style.color = "red";
        for (i=0; i<feedbackArray.length; i++) {
            feedbackArray[i].style.border = "1px solid red";
        }
        if (radio.value === "") {
            window.scrollTo(0,0);
        } else {
            feedbackArray[0].focus();
        }
        return false;
    } else if (emptyIndexArray.length !== feedbackArray.length && radio.value !== "") {
        feedbackMsg.innerHTML = "";
        for (i=0; i<feedbackArray.length; i++) {
            feedbackArray[i].style.border = "1px solid #00204E";
        }
        return true;
    } else if (emptyIndexArray.length !== feedbackArray.length && radio.value === "") {
        feedbackMsg.innerHTML = "";
        for (i=0; i<feedbackArray.length; i++) {
            feedbackArray[i].style.border = "1px solid #00204E";
        }
        window.scrollTo(0,0);
        return false;
    }
}