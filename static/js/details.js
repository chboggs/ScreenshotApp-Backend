function make_request(image_id, new_viewer) {
    var req = new XMLHttpRequest();
    var show_suggestions = function() {
        if(req.readyState == 4) {
            console.log("response:");
            console.log(req.response);
            document.getElementById("add_viewer_message").innerHTML = req.responseText;
        }
    }
    req.onreadystatechange = show_suggestions;
    req.open("POST", '/api/add_viewer?image_id=' + image_id + "&new_viewer=" + new_viewer, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send();
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function add_viewer() {
    var new_viewer = document.getElementById("add_viewer_input").value;
    var image_id = getParameterByName('image_id');

    make_request(image_id, new_viewer);
}
