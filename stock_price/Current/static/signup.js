$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var retypePassword = $('#retype-password').val();
        // Check if passwords match
        if (password !== retypePassword) {
            $('#error-message').text('Passwords do not match.');
            // Clear the password fields
            $('#password').val('');
            $('#retype-password').val('');
            return; // Stop further execution
        }
        // Send AJAX request to check if username already exists
        $.ajax({
            url: '/check_username',
            type: 'POST',
            data: { username: username },
            success: function(response) {
                if (response.exists) {
                    $('#error-message').text('Username already exists. Please choose a different username.');
                    // Clear the input fields
                    $('#username').val('');
                    $('#password').val('');
                } else {
                    // Username doesn't exist, proceed with signup
                    $.post('/signup', { username: username, password: password })
                        .done(function(response) {
                            // Redirect to login page upon successful signup
                            window.location.href = '/login';
                        })
                        .fail(function(error) {
                            $('#error-message').text('Signup failed. Please try again.');
                        });
                }
            },
            error: function() {
                $('#error-message').text('Error checking username availability. Please try again.');
            }
        });
    });
});
