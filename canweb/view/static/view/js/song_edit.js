$('document').ready(function() {
  function gotoView() {
    window.location = "/view/song/view/" + songId
  }

  function patternContent() {
    return $('#patternEdit').val();
  }

  function songLabel() {
    return $('#songLabel').val()
  }

  function submitFromEdit() {
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
        showSnackbar("Unable to submit. Label must not be empty.");
        // alert("unable to submit.")
        // alert(JSON.stringify(XMLHttpRequest));
        // alert(JSON.stringify(textStatus));
        // alert(JSON.stringify(errorThrown)); 
      },
    });
  }

  function submitFromPreview() {
    $('#patternEdit').val($('#preview-pattern-content').text())
  }

  $('#mi-searchpattern').click(function() {
    if (!$('#mi-searchpattern').hasClass('disabled')) {
      enableSearchMode();
      loadSearchResults(songLabel());
    }
  })

  function autogrow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight + 10)+"px";
  }

  $('#patternEdit').on('keyup', function() {
    autogrow(this);
  });

  function updateMiSearchPatternEnabled() {
    if ($('#songLabel').val() == "") {
      $('#mi-searchpattern').addClass('disabled');
    } else {
      $('#mi-searchpattern').removeClass('disabled');
    }
  }

  $('#songLabel').on('keyup', updateMiSearchPatternEnabled);
  updateMiSearchPatternEnabled();

  function loadSearchResults(query) {
    $('#spinner-search-results').attr('hidden', false);
    $('#search-results').attr('hidden', true);
    $('#no-search-results').attr('hidden', true);
    function searchResultItem(val) {
      item = "<tr class='song-row' data-url='" + val['url'] + "'> \
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
          $('.song-row').click(function() {
            getPattern($(this).data('url'));
          });
        } else {
          $('#no-search-results').text('No results.');
          $('#no-search-results').attr('hidden', false);
        }
      },
      error: function() {
        $("#spinner-search-results").attr('hidden', true)
        $('#no-search-results').text('Something went wrong.');
        $('#no-search-results').attr('hidden', false);
      }
    });
  }

  function getPattern(patternurl) {
    $('#spinner-search-results').attr('hidden', false);
    $("#search-pattern-mode").attr('hidden', true)
    var url = "/api/pattern/ultimateguitar/" + btoa(patternurl) + "/";
    $.ajax({
      "method": "GET",
      "url": url,
      success: function(ajaxResult) {
        $('#spinner-search-results').attr('hidden', true);
        ajaxResult = JSON.parse(ajaxResult);
        var pattern = ajaxResult['pattern'];
        enablePreviewMode(pattern);
      },
      error: function() {
        $('#spinner-search-results').attr('hidden', true);
        // alert("fail");
        enableSearchMode();
      }
    });
  }

  function enableEditMode() {
    $('#edit-mode').attr('hidden', false);
    $('#search-pattern-mode').attr('hidden', true);
    $('#preview-pattern-mode').attr('hidden', true);
    $('#mi-searchpattern').attr('hidden', false);
    $('#mi-submit').attr('hidden', false);
    $('#mi-remove').attr('hidden', false);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    autogrow($('#patternEdit')[0]);
    miCancel.click(function() {
      gotoView();
    });

    miSubmit = $('#mi-submit');
    miSubmit.unbind('click');
    miSubmit.click(function() {
      submitFromEdit();
    });
  }

  function enableSearchMode() {
    $('#edit-mode').attr('hidden', true);
    $('#search-pattern-mode').attr('hidden', false);
    $('#preview-pattern-mode').attr('hidden', true);
    $('#mi-searchpattern').attr('hidden', true);
    $('#mi-submit').attr('hidden', true);
    $('#mi-remove').attr('hidden', true);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    miCancel.click(function() {
      enableEditMode();
    });
  }

  function enablePreviewMode(previewPattern) {
    $('#edit-mode').attr('hidden', true);
    $('#search-pattern-mode').attr('hidden', true);
    $('#preview-pattern-mode').attr('hidden', false);
    $('#mi-searchpattern').attr('hidden', true);
    $('#mi-submit').attr('hidden', false);
    $('#mi-remove').attr('hidden', true);
    
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    miCancel.click(function() {
      enableSearchMode();
    });
    $('#preview-pattern-content').text(previewPattern);
    
    miSubmit = $('#mi-submit');
    miSubmit.unbind('click');
    miSubmit.click(function() {
      submitFromPreview();
      enableEditMode();
    });
  }
  enableEditMode();

  $('#mi-remove').click(function() {
    $.ajax({
      method: 'DELETE',
      url: '/api/song/' + songId + '.json',
      crossDomain: true,
      dataType: "json",
      success: function(data) {
        window.location = '/view/song/list'
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        // alert("unable to remove.")
      },
    });
  });
});