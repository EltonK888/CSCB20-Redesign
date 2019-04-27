// get text inputs from the form
let firstName = document.forms['sign_up']['first_name'];
let lastName = document.forms['sign_up']['last_name'];
let username = document.forms['sign_up']['username'];
let password = document.forms['sign_up']['password'];
let confPassword = document.forms['sign_up']['confirm_password'];
let role = document.forms['sign_up']['role'];

// get the hidden error div that will show when submission error
let firstNameError = document.getElementById("first_name_error");
let lastNameError = document.getElementById("last_name_error");
let usernameError = document.getElementById("username_error");
let passwordError = document.getElementById("password_error");
let confPasswordError = document.getElementById("conf_password_error");
let roleError = document.getElementById("role_error");

// event listeners for when the error raised after submission is fixed
firstName.addEventListener('blur', firstNameCheck);
lastName.addEventListener('blur', lastNameCheck);
username.addEventListener('blur', usernameCheck);
password.addEventListener('blur', passwordCheck);
confPassword.addEventListener('blur', confPasswordCheck);



// Submission validation to check if the form is valid
function Validate() {
    // check if first name is empty
    if (firstName.value === "") {
        firstName.style.border = "1px solid red";
        document.getElementById('firstname').style.color = "red";
        firstNameError.textContent = "First Name is required";
        firstName.focus();
        return false;
    }
    // check if last name is empty
    if (lastName.value === "") {
        lastName.style.border = "1px solid red";
        document.getElementById('lastname').style.color = "red";
        lastNameError.textContent = "Last Name is required";
        lastName.focus();
        return false;
    }
    // check if username is empty
    if (username.value === "") {
        username.style.border = "1px solid red";
        document.getElementById('username').style.color = "red";
        usernameError.textContent = "Username is required";
        username.focus();
        return false;
    }
    // check if password is empty
    if (password.value === "") {
        password.style.border = "1px solid red";
        document.getElementById('password').style.color = "red";
        password.style.border = "1px solid red";
        passwordError.textContent = "Password is required";
        password.focus();
        return false;
    }
    // check if a role is selected
    if (!(document.getElementById('student').checked) && !(document.getElementById('instructor').checked)) {
        document.getElementById('role').style.color = "red";
        roleError.textContent = "Please select a role"
        return false;
    } else {
        document.getElementById('role').style.color = "black";
        roleError.innerHTML = "";
    }
    // check if the confirmation password matches
    if (password.value != confPassword.value) {
        password.style.border = "1px solid red";
        document.getElementById('password').style.color = "red";
        document.getElementById('confpassword').style.color = "red";
        confPassword.style.border = "1px solid red";
        confPasswordError.innerHTML = "The two passwords do not match";
        confPassword.focus();
        return false;
    }


}

// event handler functions
function firstNameCheck() {
    // if not empty, then the field will go back to normal
    if (firstName.value !== "") {
        firstName.style.border = "1px solid #00204E";
        document.getElementById('firstname').style.color = "black";
        firstNameError.innerHTML = "";
        return true;
    }
}
function lastNameCheck() {
    // if not empty, then the field will go back to normal
    if (lastName.value !== "") {
        lastName.style.border = "1px solid #00204E";
        document.getElementById('lastname').style.color = "black";
        lastNameError.innerHTML = "";
        return true;
    }
}

function usernameCheck() {
    // if not empty, then the field will go back to normal
    if (username.value !== "") {
        username.style.border = "1px solid #00204E";
        document.getElementById('username').style.color = "black";
        usernameError.innerHTML = "";
        return true;
    }
}

function passwordCheck() {
    // if not empty, then the field will go back to normal
    if (password.value !== "") {
        password.style.border = "1px solid #00204E"
        document.getElementById('password').style.color = "black";
        passwordError.innerHTML = "";
        return true;
    }
    if (password.value === password_confirm.value) {
        password.style.border = "1px solid #00204E";
        document.getElementById('confpassword').style.color = "black";
        password_error.innerHTML = "";
        return true;
    }
}

function confPasswordCheck() {
    // if not empty, then the field will go back to normal
    if (confPassword.value !== "") {
        confPassword.style.border = "1px solid #00204E"
        document.getElementById('confpassword').style.color = "black";
        confPasswordError.innerHTML = "";
        return true;
    }
}

// if they have a account, then redirect to login page
document.getElementById("login").onclick = function() {
    location.href = 'login';
}

// on submission, check if the form is valid
document.getElementById("sign_up_form").onsubmit = function() {
    return Validate()
};
