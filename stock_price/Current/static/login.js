$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        
        // Get the values of username and password from the form
        var username = $('#username').val();
        var password = $('#password').val();

        // Send a POST request to the server to check the login credentials
        $.ajax({
            url: '/check_login_credentials',
            type: 'POST',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                console.log(response)
                if (response.redirect_url) {
                    var portfolioData = response.portfolio_data || [];
                    var tickerList = response.ticker_list || [];
                    // Clear the existing ticker list from local storage
                    localStorage.removeItem('tickers');
                    // Store the ticker list in local storage
                    localStorage.setItem('tickers', JSON.stringify(tickerList));

                    window.location.href = response.redirect_url;
                } else {
                    // If login credentials are invalid, render login.html with error message
                    $('#error-message').text('Invalid username or password. Please try again.');
                    // Clear the input fields
                    $('#username').val('');
                    $('#password').val('');
                }
            },
            error: function(xhr, status, error) {
                // If an error occurs, display an error message
                $('#username').val('');
                $('#password').val('');
                $('#error-message').text('Error logging in. Please try again.');
            }
        });
    });
});
