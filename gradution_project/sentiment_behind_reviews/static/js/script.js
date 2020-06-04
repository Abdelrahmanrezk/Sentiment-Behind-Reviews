

function text_gerator(){
	/*
		a function used to add text in html with funny css style
	*/
	var text_content = 'Our Project is to classify reviews that other clients leaf on some product and predict each\
     of these reviews as positive or negative.'
	sentence = "",
	char_index = 0,
	interval = setInterval(append_text, 90),
	color_index= 0;

function append_text(){
	/*
	a function here is we append these generated text using the text_content to add char by char
	*/
  sentence += text_content[char_index];
  $('.home_page .content .text_content').text(sentence).css("color", "white");
  char_index++;
  color_index++;
  if(color_index == 2) color_index = 0;
  if (char_index == text_content.length) {
    clearInterval(interval);
  }
}

}

function scrolling_behavior(){
	$("body").toggleClass("scrolling_behavior")
}
$(document).ready(function(){
	/*
		This is function called when the page is loaded automatic 
		and call text_gerator function
	*/
	text_gerator();
	
	var clicked = 0;

	$('#nav-icon').click(function(){
		scrolling_behavior();
		var $this =  $(this);
		if(!clicked){
			clicked = 1;
			// $(".main-slider").toggleClass("go-back");
			$this.toggleClass('open');
			$this.next().toggleClass("animated");
			setTimeout(function(){ 
				clicked = 0;
			}, 900);
		}
		
	});	
});	

// $('.main_product_style .product_reviews').click(function(e){
// 		e.preventDefault();
// 		var form = $(this),
//         product_id = form.attr('product_id');
//         csrfmiddlewaretoken = $(".products").find('input[name="csrfmiddlewaretoken"]').val();
//         // alert((product_id));
//         // alert((csrfmiddlewaretoken));
		
// 	  $.ajax({
//             url: '/products/reviews', // ipdate at the same url
//             method: 'POST',
//             headers: {
//                 // Secure key for forms its common for django
//                 'X-CSRFToken': csrfmiddlewaretoken,
//             },
//             data: JSON.stringify({'product_id': product_id}),
//             success: function (data) {
            	
//             	alert("suuuuuuu")
//               alert(data['product_id']);
//               window.location.href = '/products/reviews';
//               $('.reviews_page').append("<h1>Hello Review</h1>");
//             }
//         })

	
// });

$(document).ready(function(){
	$(".login_page .login_form .submit_login").click(function (e){
		e.preventDefault();
		 var username    = $('.login_page .login_form').find('input[name="username"]').val(),
		 password    = $('.login_page .login_form').find('input[name="password"]').val(),
	    csrfmiddlewaretoken   = $(".login_page .login_form").find('input[name="csrfmiddlewaretoken"]').val();
	    $('.login_page .login_error').empty();
	    $('.login_page .login_error').removeClass('alert alert-danger');
		$.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
            	'username': username,
            	'password': password,

            	}),
            success: function (data) {

            	if(data['username']){
            		window.location.href = "http://localhost:8000";
            	}else{
            		if(!username || !password){
            			$('.login_page .login_error').append("Please fill your data");
            			$('.login_page .login_error').addClass('alert alert-danger');

            		}else{
            			$('.login_page .login_error').addClass('alert alert-danger');
            			$('.login_page .login_error').append("You do not have an account with this e-mail");
            		}
            	}
            	
            }
        })
	})


	/*----------------------------------------------------------------*/

	$(".signup_page .signup_form .submit_form").click(function (e){
		e.preventDefault();
		 var first_name    = $('.signup_page .signup_form').find('input[name="first_name"]').val(),
		 	last_name    = $('.signup_page .signup_form').find('input[name="last_name"]').val(),
		 	username    = $('.signup_page .signup_form').find('input[name="username"]').val(),
		 	password1    = $('.signup_page .signup_form').find('input[name="password1"]').val(),
		 	password2    = $('.signup_page .signup_form').find('input[name="password2"]').val(),
	    csrfmiddlewaretoken   = $(".signup_page .signup_form").find('input[name="csrfmiddlewaretoken"]').val();
	    $('.signup_page .signup_error').removeClass('alert alert-danger');
	    $('.signup_page .signup_error').empty();
		
        $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
            	'first_name': first_name,
            	'last_name': last_name,
            	'username': username,
            	'password1': password1,
            	'password2': password2,
            	'csrfmiddlewaretoken': csrfmiddlewaretoken,

            	}),
            success: function (data) {
            	if(data['errors']){
            		if(!first_name || !username || !password1 || !password2) {
            			$('.signup_page  .signup_error').append("Fill Your data please");
                        $('.signup_page  .signup_error').addClass('alert alert-danger');
            		}else{
            			$('.signup_page  .signup_error').append("Invalid E-mail or password matching");
            		}     $('.signup_page  .signup_error').addClass('alert alert-danger');
            	}else{
            		window.location.href = "http://localhost:8000";
            	}
            	

            }
        })
	})


/*
-------------------------------------------
*/

$(".home_page .user_input_form .submit_text").click(function (e){
        e.preventDefault();
         var user_input    = $('.home_page .user_input_form .user_input').find('textarea[name="user_text"]').val(),
        csrfmiddlewaretoken   = $(".home_page .user_input_form").find('input[name="csrfmiddlewaretoken"]').val();
        $(".home_page .submit_textarea_error").hide();
        $(".home_page .user_input_form .predicted_review").hide();
        
       if( (user_input[0] >= 'a' && user_input[0] <= 'z') || user_input[0] >= 'A' && user_input[0] <= 'Z'){
        // $(this).before("<p class=\"submit_textarea_error\">Should you write Arabic review");
        $(this).after("<p class=\"submit_textarea_error\">Should you write Arabic review</p>");
       }
        else if(!user_input){
            $(this).after("<p class=\"submit_textarea_error\">Please add review</p>");
        }else{
             $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
                'user_input': user_input,
                }),
            success: function (data) {
                if(data['Polarity'] == "Negative"){
                    $(".home_page .user_input_form .submit_btns").after("<p class=\"predicted_review\">You Review is a <span class=\"negative\">"+ data['Polarity']  +" Review</span> </p>");
                }else{
                    $(".home_page .user_input_form .submit_btns").after("<p class=\"predicted_review\">You Review is a <span class=\"positive\">"+ data['Polarity']  +" Review</span> </p>");
                }
                
                }
            })
        }
        
       
    })

    
    $(".contact_us_page .contact_us_form .submit_contact").click(function (e){
        e.preventDefault();
         var message    = $('.contact_us_page .contact_us_form').find('textarea[name="message"]').val(),
         phonenumber    = $('.contact_us_page .contact_us_form').find('input[name="phonenumber"]').val(),
         mail    = $('.contact_us_page .contact_us_form').find('input[name="mail"]').val(),
         first_name    = $('.contact_us_page .contact_us_form').find('input[name="first_name"]').val(),
        csrfmiddlewaretoken   = $(".contact_us_page .contact_us_form").find('input[name="csrfmiddlewaretoken"]').val();
        $(".contact_us_page .submit_contact_error").hide();
        if(!message || !phonenumber){
            $(this).before("<p class=\"submit_contact_error\">Please complete form data</p>");
        }else{
            var email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i,
            phonenumber_regex = /[0-9]{11}/;
            if(!email_regex.test(mail) && mail){
            $(this).before("<p class=\"submit_contact_error\">this is not valid email</p>");
            }else if(!phonenumber_regex.test(phonenumber) && phonenumber){
                 $(this).before("<p class=\"submit_contact_error\">This is not valid phone number valid number as 01116259370 with 11 number</p>");
            }else{
                 $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
                'message': message,
                'phonenumber': phonenumber,
                'mail': mail,
                'first_name': first_name,
                }),
            success: function (data) {
               
               window.location.href = "http://localhost:8000";
                }
            })

            }
        }
        
       
    })


});	