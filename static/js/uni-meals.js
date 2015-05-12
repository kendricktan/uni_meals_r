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
$('#form-signup').on('submit', function(event){
    event.preventDefault(); // Won't refresh page
    //console.log("form submitted!")  // sanity check    
    add_user(); // Involes the add_user function
});

// Submit log-in form
$('#form-login').on('submit', function(event){
    event.preventDefault(); // Won't refresh page
    //console.log("Log in attempted!");
    login_user()
});

// Sign up and add user into the database
function add_user(){
    //console.log("adding user!");
    
    var username = document.getElementById("username-field").value;
    var email = document.getElementById("email-field").value;
    var reemail = document.getElementById("reemail-field").value;
    var password = document.getElementById("password-field").value;
    var repassword = document.getElementById("repassword-field").value;
    
    document.getElementById("username-error").innerHTML = "";
    document.getElementById("email-error").innerHTML = "";
    document.getElementById("reemail-error").innerHTML = "";
    document.getElementById("password-error").innerHTML = "";
    document.getElementById("repassword-error").innerHTML = "";
    
    // Checks email validity
    if(!is_email(email)){
        document.getElementById("email-error").innerHTML = "Please enter a valid email!";
        return false;
    }
    
    // Checks if emails are the same
    if(email != reemail){
        document.getElementById("reemail-error").innerHTML = "Emails aren't the same!";
        return false;
    }
    
    // Checks if passwords are the same
    if(password != repassword){
        document.getElementById("repassword-error").innerHTML = "Passwords aren't the same!";
        return false;
    }
    
    
    // if passes the check points then it pushes the form to the server
    $.ajax({
        url: "/signup/adduser/",  // URL to adduser
        type: "POST",  // http method... (change this later)
        
        // data to send
        data:{
            username: username,  // username value
            email: email, // email value
            password: password,  // password value
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,    // csrf token
        },
        
        // handle a successful response
        success: function(json){
            // If server posted no errors
            if(json.error == null){
                document.getElementById("form-wrapper").innerHTML = "User added! Return <a href='/'>home</a>"
            }
            
            // If we have errors
            else{
                // If the error is username related
                if(json.error == "Username"){
                    document.getElementById("username-error").innerHTML = "Username exists!";
                }
                
                // If the error is email related
                else{
                    document.getElementById("email-error").innerHTML = "Email exists!";
                }
            }
            //console.log(json.username + " added!");            
        },
        
        // handle a non-successful response
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });                  
}

function login_user(){
    // We're allowing the user to log in with email OR username
    var username_or_email = document.getElementById("username-email-field").value;
    var username = "";
    var email = "";
    var password = document.getElementById("password-field").value;
    
    // Checks if user inputted email or their usename
    var isEmail = is_email(username_or_email);    
    
    if(isEmail){
        email = username_or_email;
    }
    else{
        username = username_or_email;
    }
    
    $.ajax({
        url: "/login/loginuser/",   // URL to log user in
        type: "POST",   // http method... (change this later)
        
        // data to send
        data:{
            username: username,
            email: email,
            password: password,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,    // csrf token
        },
        
        // handle a successful response
        success: function(json){
            // Checks if successfully logged user in
            if(json.error == null){
                document.location.href = '/';
            }
            else{
                document.getElementById("login-details-error").innerHTML = "Please check your login details";
            }
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

/* End forms */
