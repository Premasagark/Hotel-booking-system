const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});


function user_login() {

    const given_email = $('#email_login').val();
    const given_password = ($('#password_login').val());
    // console.log(given_password)
    if (given_email == "" || given_password == "") {
        alert('Please enter the login credentials')
    }
    else {
        $.ajax({
            type: "POST",
            url: '/auth/user/login',
            contentType: "application/json",
            data: JSON.stringify({
                data: {
                    'email': given_email,
                    'password': given_password,
                },
                "role": "user",
            }),
            dataType: "json",
            success: function (response) {
                // console.log(response)
                // alert(response['msg']);
                window.location.replace("/home")
            },
            error: function (response) {
                alert(response['responseJSON']['error']);
            }
        });

    }

    // console.log(given_email, given_password);

}

function user_register() {

    // const given_email = $('#email_signup').val();
    const given_password = ($('#password_signup').val());
    const repeat_password = ($('#password_confirmation_signup').val())

    // console.log(given_password)
    if (given_password == '' || given_password != repeat_password) {
        alert('Please enter Password correctly ');
    } else {
        $.ajax({
            type: "POST",
            url: '/auth/user/signup',
            data: JSON.stringify({
                'data': {
                    'username': ($('#username_signup').val()),
                    'email': ($('#email_signup').val()),
                    'password': given_password,
                    'phone_number': ($('#phone_number_signup').val()),
                },
                "role": "user",
            }),
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                console.log(response)
                // alert(response['msg']);
                window.location.replace("/home")
            },
            error: function (response) {
                alert(response['responseJSON']['error']);
            }
        });

    }

    // console.log(given_email, given_password);

}