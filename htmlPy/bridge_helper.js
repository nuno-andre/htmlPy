var stripslashes = function (e) {
    if (e.substr(-1) === "/") {
        return stripslashes(e.substr(0, e.length - 1));
    }
    if (e.substr(0, 1) === "/") {
        return stripslashes(e.substr(1, e.length));
    }
    return e;
};
var link_catch = function (e) {
    e.preventDefault();
    var elem = e.target || e.srcElement;
    var call = elem.getAttribute("data-href");
    if (call === null) return;
    var params = elem.getAttribute("data-params");
    params = params !== null ? params : "";
    call = stripslashes(call);
    var exec = call.replace("/", ".");
    eval(exec + "('" + params + "')");
};
var form_catch = function (e) {
    e.preventDefault();
    var elem = e.target || e.srcElement;
    var action = elem.getAttribute("data-action");
    if (action === null) return;
    window.formdata = {};
    for (var i = 0, ii = elem.length; i < ii; ++i) {
        var input = elem[i];
        if (input.name) {
            window.formdata[input.name] = input.value;
            if (input.type === "file") {}
        }
    }
    action = stripslashes(action);
    var params = elem.getAttribute("data-params");
    var exec = action.replace("/", ".");
    exec = exec + "('" + JSON.stringify(window.formdata);
    exec = params !== null ? exec + "', '" + params + "')" : exec + "')";
    eval(exec);
};
var file_dialog = function (e) {
    e.preventDefault();
    var t = e.target.getAttribute("data-display");
    var n = e.target.getAttribute("data-filter");
    n = n !== null && n !== "null" ? n : "Any file (*.*)";
    var r = BridgeHelper.file_dialog(n);
    document.getElementById(t).value = r;
    return false;
};

setInterval(function(){
    var anchors = document.getElementsByTagName("a");
    var forms = document.getElementsByTagName("form");
    for (var i = anchors.length - 1; i >= 0; i--) {
        if(!anchors[i].classList.contains("htmlpy-activated")){
            anchors[i].onclick = link_catch;
            anchors[i].classList.add("htmlpy-activated");
        }
    }
    for (var fi = forms.length - 1; fi >= 0; fi--) {
        if(!forms[fi].classList.contains("htmlpy-activated")){
            forms[fi].onsubmit = form_catch;
            elem = forms[fi];
            for (i = 0, ii = elem.length; i < ii; ++i) {
                var input = elem[i];
                if (input.type === "file") {
                    var fileboxname = input.getAttribute("name");
                    var filter = input.getAttribute("data-filter");
                    var disabledInput = document.createElement("input");
                    disabledInput.setAttribute("disabled", "disabled");
                    disabledInput.setAttribute("name", fileboxname);
                    disabledInput.setAttribute("id", fileboxname + "_path");
                    input.parentNode.insertBefore(disabledInput, input.nextSibling);
                    var button = document.createElement("button");
                    button.innerHTML = "Choose file";
                    button.setAttribute("data-display", fileboxname + "_path");
                    button.setAttribute("data-filter", filter);
                    button.onclick = file_dialog;
                    input.parentNode.insertBefore(button, disabledInput.nextSibling);
                    input.style.display = "none";
                    elem[i].remove();
                }
            }
            forms[fi].classList.add("htmlpy-activated");
        }
    }
}, 100);
