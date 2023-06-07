// JavaScript code to show the cookie confirmation pop-up and freeze the page
$(document).ready(function() {
    $('#cookieModal').modal('show');
    $('body').addClass('modal-open');
});

$('#acceptCookies').click(function() {
    // Handle accept cookies action here
    $('#cookieModal').modal('hide');
    $('body').removeClass('modal-open');
});

// $('#declineCookies').click(function() {
//     // Handle decline cookies action here
//     $('#cookieModal').modal('hide');
//     $('body').removeClass('modal-open');
// });
