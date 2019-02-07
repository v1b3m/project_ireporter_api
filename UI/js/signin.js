document.getElementById('login-form').addEventListener('submit', loginUser)

const url = 'https://andelaireporterapp.herokuapp.com/auth/login'

function loginUser(event) {
    event.preventDefault()
    let email = document.getElementById('email')
    let password = document.getElementById('password')

    let info = document.getElementById('info-messages')
    let token = sessionStorage.getItem('token')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token},
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 200) {
            window.location.replace('./index.html')
            sessionStorage.setItem('token', data.data[0].token)
        } else {
            info.parentElement.style.display='block';
            info.textContent = ""+data.error;
        }
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}