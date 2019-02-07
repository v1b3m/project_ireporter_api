document.getElementById('registration-form').addEventListener('submit', registerNewUser)

const url ='https://andelaireporterapp.herokuapp.com/auth/register'

function registerNewUser(event) {
    event.preventDefault()
    let firstname = document.getElementById('firstname')
    let lastname = document.getElementById('lastname')
    let othernames = document.getElementById('othernames')
    let username = document.getElementById('username')
    let email = document.getElementById('email')
    let phone_number = document.getElementById('phone_number')
    let password = document.getElementById('password')

    let info = document.getElementById('info-messages')
    let token = sessionStorage.getItem('token')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token},
        body: JSON.stringify({
            username: username.value,
            email: email.value,
            phone_number: phone_number.value,
            password: password.value,
            othernames: othernames.value,
            lastname: lastname.value,
            firstname: firstname.value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 201){
            window.location.replace('./signin.html')
        } else {
            info.parentElement.style.display='block';
            info.textContent = ""+data.error;
        }
        console.log(data)
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}