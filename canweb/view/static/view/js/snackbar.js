function showSnackbar(text) {
  $("#snackbar").text(text);
  $("#snackbar").addClass('show');
  setTimeout(function() {
    $("#snackbar").removeClass('show');
  }, 3000);
}