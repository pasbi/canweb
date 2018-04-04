function loadSongList(ajaxResult) {
  items = [];
  $.each(ajaxResult, function(i, val) {
    items.push( "<li"
                + " onclick='viewSong(" + val['pk'] + ")'"
                + " class='list-group-item clearfix song-item'"
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
  var viewurl = '/view/song/view/' + songId + "/";
  $.ajax({
    url: '/api/program/' + songId,
    crossDomain: true,
    method: "GET",
    success: function(result) {
      window.location = viewurl;
    },
    error: function() {
      window.location = viewurl;
    }
  });
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

    $('#title-text').text("List");

    function applyFilter(text) {
      var listItems = $("#song-list li");
      listItems.each(function(i, li) {
        var isHidden = $(li).text().search(new RegExp(text, 'i')) == -1;
        $(li).attr('hidden', isHidden);
      });
    }

    $('#search-field').on('keyup', function() {
      applyFilter($(this).val())
    })
});