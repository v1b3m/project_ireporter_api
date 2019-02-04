document.getElementById('registration-form').addEventListener('submit', registerNewUser)

const url ='http://127.0.0.1:5000/auth/register'

function registerNewUser(event) {
    event.preventDefault()
    let firstname = document.getElementById('firstname')
    let lastname = document.getElementById('lastname')
    let othernames = document.getElementById('othernames')
    let username = document.getElementById('username')
    let email = document.getElementById('email')
    let phone_number = document.getElementById('phone_number')
    let password = document.getElementById('password')

    // let info = document.getElementById('info')
    let token = localStorage.getItem('token')

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
            window.location.replace('./index.html')
        } else {

        }
        console.log(data)
    })
    .catch((err) =>console.log(err))
}