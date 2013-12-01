var anchors = document.getElementsByTagName("a");
var forms = document.getElementsByTagName("form");

var stripslashes = function (str) {
    if(str.substr(-1) === "/") {
        return stripslashes(str.substr(0, str.length - 1));
    }
    if(str.substr(0, 1) === "/") {
        return stripslashes(str.substr(1, str.length));
    }
    return str;
};

var link_catch = function (e) {
    e.preventDefault();
    var elem = e.target || e.srcElement;
    var call = elem.getAttribute("data-href");

    if (call === null)
        return;

    var params = elem.getAttribute("data-params");
    params = params !== null ? params : "";
    call = stripslashes(call);
    var exec = call.replace("/", ".");
    eval(exec + '(\'' + params + '\')');
};

var form_catch = function (e) {
    e.preventDefault();

    var elem = e.target || e.srcElement;
    var action = elem.getAttribute("data-action");

    if (action === null)
        return;

    window.formdata = {};
    for (var i = 0, ii = elem.length; i < ii; ++i) {
        var input = elem[i];
        if (input.name) {
            window.formdata[input.name] = input.value;

            if (input.type === "file") {
            }
        }

    }

    action = stripslashes(action);
    var params = elem.getAttribute("data-params");

    var exec = action.replace("/", ".");
    exec = exec + "('" + JSON.stringify(window.formdata);
    exec = params !== null ? exec + "', \'" + params + '\')' : exec + "')";
    eval(exec);
};

var file_dialog = function(e) {
    e.preventDefault();
    var displayID = e.target.getAttribute("data-display");
    var filter = e.target.getAttribute("data-filter");
    filter = filter !== null && filter !== "null" ? filter : "Any file (*.*)";
    var filepath = BridgeHelper.file_dialog(filter);
    document.getElementById(displayID).value = filepath;
    return false;
};

for (var i = anchors.length - 1; i >= 0; i--) {
    anchors[i].onclick = link_catch;
}

for (var i = forms.length - 1; i >= 0; i--) {
    forms[i].onsubmit = form_catch;
    elem = forms[i];

    for (var i = 0, ii = elem.length; i < ii; ++i) {
        var input = elem[i];
        if (input.type === "file") {
            var fileboxname = input.getAttribute("name");
            var filter = input.getAttribute("data-filter");
            var disabledInput = document.createElement('input');
            disabledInput.setAttribute("disabled", "disabled");
            disabledInput.setAttribute("name", fileboxname);
            disabledInput.setAttribute("id", fileboxname + "_path");
            input.parentNode.insertBefore(disabledInput, input.nextSibling);

            var button = document.createElement('button');
            button.innerHTML = "Choose file";
            button.setAttribute("data-display", fileboxname + "_path");
            button.setAttribute("data-filter", filter);
            button.onclick = file_dialog;
            input.parentNode.insertBefore(button, disabledInput.nextSibling);

            input.style.display = "none";
            elem[i].remove();
        }
    }
}