
function isLoggedIn(){
    var token = localStorage.getItem('token')
    if (token == null || token === '') {
        window.location.replace('./signin.html')
    }
}

isLoggedIn()
