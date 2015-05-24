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

// Gets csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* End useful functions */

/* Forms for authentication */
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
        document.getElementById('re_password-error').innerHTML = 'Password aren\'t the same, check again!';
        return false;
    }
    
    // if passes the check points then it pushes the form to the server
    $.ajax({
        url: "/profile/signup/",  // URL to adduser
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
                //console.log(json);
                document.getElementById("login-details-error").innerHTML = "Invalid log in details."
            }
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

/* End Forms for authentication */

/* Profile edit */
// Submit edit profile info form
$('#profile-info-form').on('submit', function(event){
    event.preventDefault(); // Won't refresh page
    //console.log("Attempted to change user info!");
    update_profile_info($(this).serialize());
});

function update_profile_info(data){
    $.ajax({        
        url: $('#data-div').attr('data-url') + 'update_info/',
        type: 'POST',
        
        data: data,
        
        success: function(json){
            //window.location.reload();
            document.getElementById('form-status-profile-info').innerHTML = "Successfully updated your details!";
            console.log("Success in changing user info");
        },
        
        error: function(xhr, errmsg, err){
            console.log("an error occured");
        }
    });
}

// Submit edit profile password form
$('#profile-pasword-form').on('submit', function(event){        
    event.preventDefault(); // Won't refresh page
    //console.log("Attempted to change user password!");
    document.getElementById('form-status-profile-password-error').innerHTML = '';
    
    if(document.getElementById('id_new_password').value == document.getElementById('id_new_re_password').value){
        update_profile_password($(this).serialize());
    }
    else{
        document.getElementById('form-status-profile-password-error').innerHTML = 'Passwords do not match';
    }    
});

function update_profile_password(data){    
    $.ajax({        
        url: $('#data-div').attr('data-url') + 'update_password/',
        type: 'POST',
        
        data: data,
        
        success: function(json){
            //window.location.reload();
            document.getElementById('form-status-profile-password').innerHTML = "Successfully updated your password!";
            console.log("Success in changing password");
        },
        
        error: function(xhr, errmsg, err){
            console.log("an error occured");
        }
    });
}

// Change user dp button
$("#btn-change-dp").click(function(){
    // Gets image data
    var val = $("#id_new_dp").val();
    
    // Checks to see if it is a suitable format
    if (!val.match(/(?:gif|jpg|png|bmp)$/)) {        
        document.getElementById('form-status-dp-error').innerHTML = 'I can only consume image files!';
        return false;
    }
    
    else{
        return true;
    }
    
})

/* End profile edit */

// Heart food
function user_heart(a_div){      
    $.ajax({
        url: $(a_div).attr('href'),    
        type: 'POST',
        data: {            
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        
        success: function(json){
            // changes it to unheart food
            var url_string = $(a_div).attr("href");
            var function_string = $(a_div).attr("onclick");            
            
            var a_div_id = $(a_div).attr("id");
            
            url_string = url_string.replace("heart", "unheart");
            function_string = function_string.replace("heart", "unheart");            
            
            document.getElementById(a_div_id).setAttribute("href", url_string);
            document.getElementById(a_div_id).setAttribute("onclick", function_string);            
            document.getElementById(a_div_id).innerHTML = '<i class="heart icon"></i>';            
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    return false;
}

function user_unheart(a_div){
    $.ajax({
        url: $(a_div).attr('href'),    
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        
        success: function(json){
            // changes it to heart food
            var url_string = $(a_div).attr("href");
            var function_string = $(a_div).attr("onclick");            
            
            var a_div_id = $(a_div).attr("id");
            
            url_string = url_string.replace("unheart", "heart");
            function_string = function_string.replace("unheart", "heart");            
            
            document.getElementById(a_div_id).setAttribute("href", url_string);
            document.getElementById(a_div_id).setAttribute("onclick", function_string);            
            document.getElementById(a_div_id).innerHTML = '<i class="empty heart icon"></i>';            
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    return false;
}

// Upvote/Downvote eatery
function eatery_vote(a_div){
    var url_string = $(a_div).attr('href');
    
    // Is user upvoting or downvoting
    var upvote = (url_string.search('upvote') != -1);    
    
    $.ajax({
        url: url_string,
        type: 'POST',
        data:{
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        
        success: function(json){
            // Change inner HTML to clear vote button
            var eatery_id = json['eatery_id'];            
            document.getElementById('div-vote-wrapper').innerHTML= '<a onclick="return eatery_clear_vote(this);" href="/profile/clearvote/eatery/'+eatery_id+'/">Clear vote</a>';            
            
            // Update vote %
            var eatery_upvote_percentage = json['eatery_upvote_all'][0][0];
            var eatery_vote_total = json['eatery_upvote_all'][0][1];
            
            if (eatery_upvote_percentage == null && eatery_vote_total == 0){
                eatery_upvote_percentage = "--";
            }
            
            else if (eatery_upvote_percentage == null){
                eatery_upvote_percentage = "0";
            }           
            
            document.getElementById('eatery-upvotes-percentage-wrapper').innerHTML = '<strong>'+eatery_upvote_percentage+'%</strong>';
            document.getElementById('eatery-votes-total-wrapper').innerHTML = eatery_vote_total + ' votes';
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    
    return false;
}

// Clear vote
function eatery_clear_vote(a_div){
    var url_string = $(a_div).attr('href');    
    $.ajax({
        url: url_string,
        type: 'POST',
        data:{
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        
        success: function(json){ 
            //console.log(json);
            
            // Change innerHTML back to Upvote/Downbote button
            var eatery_id = json['eatery_id'];  
            document.getElementById('div-vote-wrapper').innerHTML= '<a onclick="return eatery_vote(this);" href="/profile/upvote/eatery/'+eatery_id+'/"><button id="eatery-'+eatery_id+'-upvote" class="btn btn-success"><i class="glyphicon fui-triangle-up"></i></button></a><a onclick="return eatery_vote(this);" href="/profile/downvote/eatery/'+eatery_id+'/"><button id="eatery-'+eatery_id+'-downvote"class="btn btn-danger"><i class="glyphicon fui-triangle-down"></i></button></a>';
            
            // Update vote %
            try{
                var eatery_upvote_percentage = json['eatery_upvote_all'][0][0];
                var eatery_vote_total = json['eatery_upvote_all'][0][1];

                if (eatery_upvote_percentage == null && eatery_vote_total == 0){
                    eatery_upvote_percentage = "--";
                }

                else if (eatery_upvote_percentage == null){
                    eatery_upvote_percentage = "0";
                }

                document.getElementById('eatery-upvotes-percentage-wrapper').innerHTML = '<strong>'+eatery_upvote_percentage+'%</strong>';
                document.getElementById('eatery-votes-total-wrapper').innerHTML = eatery_vote_total + ' votes';
            } catch(err){
                console.log(err);
            }
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    
    return false;
}


// Review review's usefulness
function review_reviews_usefullness(a_div, is_useful){
    var div_id = $(a_div).attr('data-div-wrapper');
    var url_full_path = $(a_div).attr('data-url-path');
    
    $.ajax({
        url: $(a_div).attr('href'),
        type: 'POST',
        data:{
            is_useful: is_useful,
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        
        success: function(json){
            var eatery_id = json['eatery_id'];
            var review_id = json['review_id'];
            
            document.getElementById(div_id).innerHTML = '<a data-url-path="'+url_full_path+'" data-div-wrapper="div-review-opinion-'+review_id+'" onclick="return review_clear_usefullness(this)" href="'+url_full_path+'review/'+review_id+'/clear/">Clear opinion</a>';
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    
    return false;
}

// Clear review's usefulness
function review_clear_usefullness(a_div){
    var div_id = $(a_div).attr('data-div-wrapper');
    var url_full_path = $(a_div).attr('data-url-path');
    
    $.ajax({
        url: $(a_div).attr('href'),
        type: 'POST',
        data:{
            csrfmiddlewaretoken: getCookie('csrftoken'),            
        },
        
        success: function(json){
            var eatery_id = json['eatery_id'];
            var review_id = json['review_id'];
            
            document.getElementById(div_id).innerHTML = '<a data-url-path="'+url_full_path+'" data-div-wrapper="div-review-opinion-'+review_id+'" onclick="return review_reviews_usefullness(this, true);" style="font-size: 1.5em;" href="'+url_full_path+'review/'+review_id+'/" rel="tooltip" title="I find this useful"><i class="glyphicon fui-check"></i></a><a data-url-path="'+url_full_path+'" data-div-wrapper="div-review-opinion-'+review_id+'" onclick="return review_reviews_usefullness(this, false);" style="font-size: 1.5em; color: #C0392B" href="'+url_full_path+'review/'+review_id+'/" rel="tooltip" title="I don\'t find this useful"><i class="glyphicon fui-cross"></i></a>';
        },
        
        error: function(xhr, errmsg, err){
            console.log(xhr);
        }
    });
    return false;
}
/* End Eatery */