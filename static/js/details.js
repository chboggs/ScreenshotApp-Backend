function add_viewer_request(image_id_str, new_viewer_str) {
    var req = new XMLHttpRequest();
    var body = "image_id=" + image_id_str + "&new_viewer=" + new_viewer_str;
    var show_suggestions = function() {
        if(req.readyState == 4) {
            document.getElementById("add_viewer_message").innerHTML = req.responseText;
        }
    }
    req.onreadystatechange = show_suggestions;
    req.open("POST", '/api/add_viewer', true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(body);
}

function add_comment_request(image_id_str, comment_str) {
    var req = new XMLHttpRequest();
    var body = "image_id=" + image_id_str + "&comment=" + comment_str;
    var show_suggestions = function() {
        if(req.readyState == 4) {
            document.getElementById("add_comment_message").innerHTML = req.responseText;
        }
    }
    req.onreadystatechange = show_suggestions;
    req.open("POST", '/api/add_comment', true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(body);
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

    add_viewer_request(image_id, new_viewer);
}

function add_comment() {
    var comment = document.getElementById("add_comment_input").value;
    var image_id = getParameterByName('image_id');

    add_comment_request(image_id, comment);
}
