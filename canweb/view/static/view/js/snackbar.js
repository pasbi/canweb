function showSnackbar(id) {
    var x = document.getElementById(id)
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}