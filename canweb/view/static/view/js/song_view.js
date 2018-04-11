$('document').ready(function() {

  items = []
  items.push("<li class='nav-item'><a class='nav-link' id='mi-edit'>Edit</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-updatemidi'>🎘</a></li>");
  $('#navbar-ul').html(items.join(''))

  $('#mi-edit').click(function() {
    window.location = '/view/song/edit/' + songId + "/";
  });
  $('#mi-updatemidi').click(function() {
    $.ajax({
      url: '/api/song/' + songId + '/transmitMidiProgram',
      crossDomain: true,
      method: "GET",
      success: function() {
        showSnackbar("Sent midi command.")
      },
      error: function(error) {
        if (error.status == 500) {
          showSnackbar("Could not send midi command. Is the device connected properly?");
        } else if (error.status == 400) {
          showSnackbar("Could not send midi command. Does this song have a midi command?");
        } else {
          showSnackbar("Cannot send midi command, something went wrong.");
        }
        theError = error
      }
    });
  });
});