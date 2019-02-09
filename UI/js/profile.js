var token = sessionStorage.getItem('token')
let info = document.getElementById('info-messages')

function myProfile(){
    const url = 'https://andelaireporterapp.herokuapp.com/user'

    fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    })
    .then((response) => response.json())
    .then((data) => {
        profilePic = document.getElementById('profile-pic')
        avatar = data.gravatar.concat(128)
        profilePic.innerHTML = '<img id="myAvatar" src="'+avatar+'" alt="profile pic">'
        username = document.getElementById('username')
        username.innerHTML = data.username
        username = document.getElementById('user')
        username.innerHTML = data.username
        firstname = document.getElementById('firstname')
        firstname.innerHTML = data.firstname
        lastname = document.getElementById('lastname')
        lastname.textContent = data.lastname
        registered = document.getElementById('registered')
        registered.textContent = data.registered
        email = document.getElementById('email')
        email.textContent = data.email
        othernames = document.getElementById('othernames')
        othernames.textContent = data.othernames
        phone = document.getElementById('phone')
        phone.textContent = data.phone_number
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}

function myStats(){
    const url = 'https://andelaireporterapp.herokuapp.com/user/stats'

    fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    })
    .then((response) => response.json())
    .then((data) => {
        resolvedFlags = document.getElementById('resolved-flags')
        resolvedFlags.textContent = data.resolved_flags
        resolvedInterventions = document.getElementById('resolved_interventions')
        resolvedInterventions.textContent = data.resolved_interventions
        pendingFlags = document.getElementById('pending_flags')
        pendingFlags.textContent = data.pending_flags
        pendingInterventions = document.getElementById('pending_interventions')
        pendingInterventions.textContent = data.pending_interventions
        rejectedFlags = document.getElementById('rejected_flags')
        rejectedFlags.textContent = data.rejected_flags
        rejectedInterventions = document.getElementById('rejected_interventions')
        rejectedInterventions.textContent = data.rejected_interventions
        percentSuccess = document.getElementById('percentage_success')
        percentSuccess.textContent = data.percentage_success+'%'
        percentFailure = document.getElementById('percent_failure')
        percentFailure.textContent = data.percentage_failure+'%'
        rating = document.getElementById('rating')
        stars = data.rating

        output =''
        for(let star=0; star < stars; star++) {
            output += '<span class="fa fa-star checked"></span>'
        }
        for(let blanks=0; blanks < 5 - stars; blanks++) {
            output += '<span class="fa fa-star"></span>'
        }

        rating.innerHTML = output
    })
}

myProfile()
myStats()