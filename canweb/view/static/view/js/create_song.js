$('document').ready(function() {

    // disable import button if label is empty
    updateImportButton = function() {
        var query = $("#songLabel").text();
        var importButton = document.getElementById("importButton");
        if (query == "") {
            importButton.disabled = true;
        } else {
            importButton.disabled = false;
        }
    }
    $('#songLabel').on('input', function(e) {
        updateImportButton();
    });
    updateImportButton();

    $('#editButton').click(function() {
        window.location = "song/edit"
    })
})