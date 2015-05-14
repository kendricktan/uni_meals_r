/* Initialize styling */
// Nav tab
$(document).ready(function() {
  	$('#tab-wizard').bootstrapWizard({'tabClass': 'nav nav-pills'});
});

// Tooltip
$(function () {
    $("[rel='tooltip']").tooltip();
});
/* End Initialize styling */

/* Useful functions */
// Checks if email is valid
function is_email(email){      
	var emailReg = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
	return emailReg.test(email); 
} 
/* End useful functions */

/* Forms */
// Submit sign-up form
$('#form-signup').submit(function(event){    
    event.preventDefault(); // Won't refresh page
    //console.log("Sign up attempted!")  // sanity check     
    add_user($(this).serialize()); // Involes the add_user function
});

// Submit log-in form
$('#form-login').on('submit', function(event){
    event.preventDefault(); // Won't refresh page
    //console.log("Log in attempted!");
    login_user($(this).serialize());
});

// Sign up and add user into the database
function add_user(data){    
    // if passes the check points then it pushes the form to the server
    $.ajax({
        url: "/profile/signup/adduser/",  // URL to adduser
        type: "POST",  // http method... (change this later)
        
        // data to send
        data: data,
        
        // handle a successful response
        success: function(json){
            if(json.username != null){
                console.log(json.username + " added!");
            }
            else{
                console.log(json);
            }
        },
        
        // handle a non-successful response
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });                  
}

// Login user
function login_user(data){
    // We're allowing the user to log in with email OR username
    
    $.ajax({
        url: "/profile/login/",   // URL to log user in
        type: "POST",   // http method... (change this later)
        
        // data to send
        data: data,
        
        // handle a successful response
        success: function(json){
            // Checks if successfully logged user in
            if(json.error == null){
                // Redirects back to home page
                document.location.href = '/';
            }
            else{
                // Logs error
                console.log(json);
                //document.getElementById("login-details-error").innerHTML = "Invalid log in details, poo-face."
            }
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

/* End forms */
