function loadSongList(ajaxResult) {
  items = [];
  $.each(ajaxResult, function(i, val) {
    items.push( "<li"
                + " onclick='viewSong(" + val['pk'] + ")'"
                + " class='list-group-item clearfix'"
                + " id='song-" + val['pk'] + "'>" 
                + "</li>");
  });
  if (items.length > 0) {
    $('#song-list').html(items.join(''));
    $.each(ajaxResult, function(i, val) {
      $('#song-' + val['pk']).text(val['label']);
    });
    $('#song-list').removeAttr('hidden');
  } else {
    $('#no-songs-placeholder').removeAttr('hidden');
  }  
}

function viewSong(songId) {
  window.location = '/view/song/view/' + songId + "/";
}

function editSong(songId) {
  window.location = '/view/song/edit/' + songId + "/";
}

$('document').ready(function () {
    $.ajax({
      url: '/api/song/list.json',
      method: "GET",
      success: function(result) {
        loadSongList(result);
      }
    });

    $('#mi-create').click(function() {
      $.ajax({
        url: '/api/song/list.json',
        crossDomain: true,
        dataType: "json",
        data: { 
          label: ""
        },
        method: "POST",
        success: function(result) {
          editSong(result['pk']);
        },
        error: function() {
          alert("Unable to create song")
        }
      });
    });
});