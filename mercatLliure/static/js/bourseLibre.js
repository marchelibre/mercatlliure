$(document).ready(function() {

  $('[data-toggle="offcanvas"]').click(function() {
    $('#wrapper').toggleClass('toggled');
  });

  // Toggle the class
  $('body').on('click', '.dropdown', function() {
    $(this).toggleClass('show');
  });

});