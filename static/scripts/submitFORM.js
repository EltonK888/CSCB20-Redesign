var closedButtons = document.getElementsByClassName('mark_as_closed_btn');
var i;

// create an on click even for every non-closed remark
for (i=0; i<closedButtons.length; i++) {
    closedButtons[i].onclick = function () {
        // find which button triggered a click event and capture its id
        res = event.target.id;
        resArray = res.split(',');
        // pass to submit form
        return submitFORM('change_student_remark_request_status','post',{'student_uid': resArray[0], 'grade_name': resArray[1]});
    }
}

function submitFORM(path, method, params) {
    method = method || "post"; 
    // Create a form element
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    //Move the submit function to another variable
    //so that it doesn't get overwritten.
    form._submit_function_ = form.submit;

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            // Hide input field
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form._submit_function_();
}