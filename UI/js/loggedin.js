
function isLoggedIn(){
    var token = sessionStorage.getItem('token')
    if (token == null || token === '') {
        window.location.replace('./signin.html')
    }
}

isLoggedIn()
