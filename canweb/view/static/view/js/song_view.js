$('document').ready(function() {
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