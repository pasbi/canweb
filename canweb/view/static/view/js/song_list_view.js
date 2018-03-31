function loadSongList(ajaxResult) {
  items = [];
  $.each(ajaxResult, function(i, val) {
    items.push( "<li"
                + " onclick='viewSong(" + val['pk'] + ")'"
                + " class='list-group-item clearfix'"
                + ">" 
                + val['label']
                + "</li>");
  });
  if (items.length > 0) {
    $('#song-list').html(items.join(''));
    $('#song-list').removeAttr('hidden');
  } else {
    $('#no-songs-placeholder').removeAttr('hidden');
  }
}

function viewSong(songId) {
  window.location = '/view/song/view/' + songId + "/";
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
          label: "Unnamed Song"
        },
        method: "POST",
        success: function(result) {
          viewSong(result['pk']);
        },
        error: function() {
        }
      });
    });
});