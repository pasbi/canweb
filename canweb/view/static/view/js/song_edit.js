$('document').ready(function() {

  items = [];
  items.push("<li class='nav-item'><a class='nav-link' id='mi-submit'>✓</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-cancel'>✗</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-searchpattern'>🔎</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-remove'>🗑</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-trup'>♯</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-trdown'>♭</a></li>");
  items.push("<li class='nav-item'><a class='nav-link' id='mi-toggle-program-edit'>🎘</a></li>");
  $('#navbar-ul').html(items.join(''))
  // $('#mi-updatemidi').addClass('dropdown-menu');

  $("#mi-toggle-program-edit").click(function() {
    var ep = $("#edit-program")
    if (ep.is(":visible")) {
      ep.hide()
    } else {
      ep.show()
      try {
        $('#isValidCheckbox').prop('checked', songProgram['isValid'])
        $('#select-bank option').removeAttr("selected");
        $('#select-bank option:eq(' + songProgram['bank'] + ')').attr('selected', 'selected');
        $('#select-page option').removeAttr("selected");
        $('#select-page option:eq(' + songProgram['page'] + ')').attr('selected', 'selected');
        $('#select-program option').removeAttr("selected");
        $('#select-program option:eq(' + songProgram['program'] + ')').attr('selected', 'selected');
      } catch (error) {
        alert("X")
        console.log(error);
      }
    }
  });

  function gotoView() {
    window.location = "/view/song/view/" + songId
  }

  function patternContent() {
    var patternEdit = $('#patternEdit');
    if (arguments.length == 1) {
      patternEdit.val(arguments[0]);
    } else {
      return patternEdit.val();
    }
  }

  function songLabel() {
    return $('#songLabel').val()
  }

  function submitFromEdit() {

    program = {
      "bank": $('#select-bank option:selected').index(),
      "program": $('#select-program option:selected').index(),
      "page": $('#select-page option:selected').index(),
      "type": "NS2",
      "isValid": $('#isValidCheckbox').prop('checked')
    };

    $.ajax({
      method: 'PUT',
      url: '/api/song/' + songId + '.json',
      crossDomain: true,
      dataType: "json",
      data: { 
        label: songLabel(), 
        pattern: patternContent(),
        midiCommand: JSON.stringify(program),
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

  $('#mi-searchpattern').click(function() {
    if (!$('#mi-searchpattern').hasClass('disabled')) {
      enableSearchMode();
      loadSearchResults(songLabel());
    }
  })

  function autogrow(element) {
    var sx = window.scrollX;
    var sy = window.scrollY;
    element.style.height = "5px";
    element.style.height = (element.scrollHeight + 10)+"px";
    window.scrollTo(sx, sy);
  }

  $('#patternEdit').on('keyup', function() {
    autogrow(this);
  });

  function updateMiNavBarEnabled() {
    if ($('#songLabel').val() == "") {
      $('#mi-searchpattern').addClass('disabled');
      $('#mi-submit').addClass('disabled');
    } else {
      $('#mi-searchpattern').removeClass('disabled');
      $('#mi-submit').removeClass('disabled');
    }
  }

  $('#songLabel').on('keyup', updateMiNavBarEnabled);
  $('#patternEdit').on('keyup', updateMiNavBarEnabled);
  updateMiNavBarEnabled();

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
    $('#mi-trup').attr('hidden', false);
    $('#mi-trdown').attr('hidden', false);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    autogrow($('#patternEdit')[0]);
    miCancel.click(function() {
      if (justCreated) {
        deleteSong();
      } else {
        gotoView();
      }
    });

    miSubmit = $('#mi-submit');
    miSubmit.unbind('click');
    miSubmit.click(function() {
      if (!$('#mi-submit').hasClass('disabled')) {
        submitFromEdit();
      }
    });

    $('#title-text').text("Edit");
  }

  function enableSearchMode() {
    $('#title-text').text("Search '" + songLabel() + "'");
    $('#edit-mode').attr('hidden', true);
    $('#search-pattern-mode').attr('hidden', false);
    $('#preview-pattern-mode').attr('hidden', true);
    $('#mi-searchpattern').attr('hidden', true);
    $('#mi-submit').attr('hidden', true);
    $('#mi-remove').attr('hidden', true);
    $('#mi-trup').attr('hidden', true);
    $('#mi-trdown').attr('hidden', true);
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    miCancel.click(function() {
      enableEditMode();
    });
  }

  function enablePreviewMode(previewPattern) {
    $('#title-text').text("Preview " + "");
    $('#edit-mode').attr('hidden', true);
    $('#search-pattern-mode').attr('hidden', true);
    $('#preview-pattern-mode').attr('hidden', false);
    $('#mi-searchpattern').attr('hidden', true);
    $('#mi-submit').attr('hidden', false);
    $('#mi-remove').attr('hidden', true);
    $('#mi-trup').attr('hidden', true);
    $('#mi-trdown').attr('hidden', true);
    
    miCancel = $('#mi-cancel');
    miCancel.unbind('click');
    miCancel.click(function() {
      enableSearchMode();
    });
    $('#preview-pattern-content').text(previewPattern);
    
    miSubmit = $('#mi-submit');
    miSubmit.unbind('click');
    miSubmit.click(function() {
      patternContent($('#preview-pattern-content').text())
      enableEditMode();
    });
  }
  enableEditMode();

  function deleteSong() {
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
    
  }

  $('#mi-remove').click(function() {
    deleteSong();
  });

  function transpose(d) {
    $.ajax({
      method: 'POST',
      url: '/api/transpose/' + d,
      crossDomain: true,
      dataType: "json",
      data: {
        "pattern": patternContent()
      },
      success: function(data) {
        patternContent(data["pattern"])
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
      },
    });
  }

  $('#mi-trup').click(function() {
    transpose(1);
  });
  $('#mi-trdown').click(function() {
    transpose(11);
  });
  


});
