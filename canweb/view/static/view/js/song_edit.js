$('document').ready(function() {
  function gotoView() {
    window.location = "/view/song/view/" + songId
  }

  function patternContent() {
    return $('#contentArea').val();
  }

  function songLabel() {
    return $('#song-label').text()
  }

  $('#mi-submit').click(function() {
    $.ajax({
      method: 'PUT',
      url: '/api/song/' + songId + '.json',
      crossDomain: true,
      dataType: "json",
      data: { 
        label: songLabel(), 
        pattern: patternContent()
      },
      success: function(data) {
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
  $('#mi-searchpattern').click(function() {
    enableSearchMode();
  })

  function autogrow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight + 10)+"px";
  }

  $('#contentArea').on('keyup', function() {
    autogrow(this);
  });

  function loadSearchResults(query) {
    $('#spinner-search-results').attr('hidden', false);
    $('#search-results').attr('hidden', true);
    $('#no-search-results').attr('hidden', true);
    function searchResultItem(val) {
      item = "<tr class='song-row' data-href='" + val['url'] + "'> \
                <td>" + val['song_name'] + "</td> \
                <td>" + val['artist_name'] + "</td> \
                <td>" + val['rating'] + "</td> \
              </tr>";
      return item;
    }
    var service = 'ultimateguitar';
    query = encodeURIComponent(query);
    $.ajax({
      url: '/api/search/' + service + '/' + query + '/',
      method: "GET",
      success: function(ajaxResult) {
        items = [];
        ajaxResult = JSON.parse(ajaxResult);
        r = ajaxResult;
        $.each(ajaxResult, function(i, val) {
          items.push(searchResultItem(val));
        });
        $("#spinner-search-results").attr('hidden', true)
        if (items.length > 0) {
          $('#search-results-body').html(items.join(''));
          $('#search-results').attr('hidden', false);
        } else {
          $('#no-search-results').text('No results.');
          $('#no-search-results').attr('hidden', false);
        }
      },
      error: function() {
        $("#spinner-search-results").attr('hidden', true)
        $('#no-search-results').text('Something went wrong.');
        $('#no-search-results').attr('hidden', false);y
      }
    });
  }

  function enableEditMode() {
    $('#edit-mode').attr('hidden', false);
    $('#search-pattern-mode').attr('hidden', true);
    $('#preview-pattern-mode').attr('hidden', true);
    $('#mi-searchpattern').attr('hidden', false);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    autogrow($('#contentArea')[0]);
    miCancel.click(function() {
      gotoView();
    });
  }

  function enableSearchMode() {
    $('#edit-mode').attr('hidden', true);
    $('#search-pattern-mode').attr('hidden', false);
    $('#preview-pattern-mode').attr('hidden', true);
    $('#mi-searchpattern').attr('hidden', true);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    miCancel.click(function() {
      enableEditMode();
    });
    loadSearchResults(songLabel());
  }
  
  enableEditMode();
});