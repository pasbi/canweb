function loadSongList(ajaxResult) {
  items = [];
  $.each(ajaxResult, function(i, val) {
    items.push( "<li"
                + " onclick='onClickSong(" + val['pk'] + ")'"
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

function onClickSong(songId) {
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
});