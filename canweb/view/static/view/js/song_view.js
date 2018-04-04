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
      url: '/api/program/' + songId,
      crossDomain: true,
      method: "GET"
    });
  });
});