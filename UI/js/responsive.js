function makeResponsive() {
    var i = document.getElementById("mynavbar");
    if (i.className == "navbar") {
        i.className += " responsive";
    } else {
        i.className = "navbar";
    }
}