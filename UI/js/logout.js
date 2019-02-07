var signOut = document.getElementById("logout")
signOut.addEventListener('click', logoutUser)

const url = 'https://andelaireporterapp.herokuapp.com/auth/logout'

function logoutUser(){
    let info = document.getElementById('info-messages')
    let token = sessionStorage.getItem('token')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.status === 200) {
            window.location.replace('./signin.html')
            sessionStorage.clear();
        } else {
            info.parentElement.style.display = 'block';
            info.textContent = data.error
        }
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}