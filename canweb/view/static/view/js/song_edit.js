$('document').ready(function() {
  function gotoView() {
    window.location = "/view/song/view/" + songId
  }
  $('#mi-cancel').click(function() {
    gotoView();
  });

  $('#mi-submit').click(function() {
    $.ajax({
      method: 'PUT',
      url: '/api/song/' + songId + '.json',
      crossDomain: true,
      dataType: "json",
      data: { 
        label: $('#song-label').text(), 
        pattern: $('#pattern-edit').text() 
      },
      success: function(data) {
        alert("put performed.")
        gotoView();
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        alert("unable to submit.")
        // alert(JSON.stringify(XMLHttpRequest));
        // alert(JSON.stringify(textStatus));
        // alert(JSON.stringify(errorThrown)); 
      },
    });
  });
});