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
    // Refreshes the fields so it doesn't confuse the user
    document.getElementById('username-error').innerHTML = '';
    document.getElementById('email-error').innerHTML = '';
    document.getElementById('re_email-error').innerHTML = '';
    document.getElementById('password-error').innerHTML = '';
    document.getElementById('password-error').innerHTML = '';
    
    // Don't want any empty fields
    if (document.getElementById('id_username').value == ''){
        document.getElementById('username-error').innerHTML = 'Username field can\'t be empty!';
        return false;
    }
    
    
    if (document.getElementById('id_email').value == ''){
        document.getElementById('email-error').innerHTML = 'Email field can\'t be empty!';
        return false;
    }
    
    if (document.getElementById('id_re_email').value == ''){
        document.getElementById('re_email-error').innerHTML = 'Re-enter email field can\'t be empty!';
        return false;
    }
    
    if (document.getElementById('id_password').value == ''){
        document.getElementById('password-error').innerHTML = 'Password field can\'t be empty!';
        return false;
    }
    
    if (document.getElementById('id_re_password').value == ''){
        document.getElementById('re-password-error').innerHTML = 'Re-enter password field can\'t be empty!';
        return false;
    } 
    
    // Checks for valid email
    if (!is_email(document.getElementById('id_email').value)){
        document.getElementById('email-error').innerHTML = 'Please enter a valid email!';
        return false;
    }
    
    // Checks if emails are the same
    if (document.getElementById('id_email').value != document.getElementById('id_re_email').value){
        document.getElementById('re_email-error').innerHTML = 'Emails aren\'t the same, check again!';
        return false;
    }
    
    // Checks if passwords are the same
    if (document.getElementById('id_password').value != document.getElementById('id_re_password').value){
        document.getElementById('re_password-error').innerHTML = 'Emails aren\'t the same, check again!';
        return false;
    }
    
    // if passes the check points then it pushes the form to the server
    $.ajax({
        url: "/profile/signup/adduser/",  // URL to adduser
        type: "POST",  // http method... (change this later)
        
        // data to send
        data: data,
        
        // handle a successful response
        success: function(json){
            if(json.username != null){
                //console.log(json.username + " added!");
                document.getElementById('div-form-signup').innerHTML = json.username + ' signed up successfully, please <a href="/profile/login">login</a> or return to <a href="/">home</a>';
            }
            else if(json.error == 'username'){
                document.getElementById('username-error').innerHTML = 'Username already taken, please try another username';
            }
            else if(json.error == 'email'){
                document.getElementById('email-error').innerHTML = 'Email already taken, please try another email';
            }
            else{
                alert('An error occured, please refresh the page and try signing up again!');
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
