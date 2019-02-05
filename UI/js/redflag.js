var frm = document.getElementById('red-flag-form')
frm.addEventListener('submit', createRedflag)

const url = 'https://andelaireporterapp.herokuapp.com/api/v2/red-flags'

function createRedflag(event) {
    event.preventDefault()
    let title = document.getElementById('title')
    let location = document.getElementById('location')
    let comment = document.getElementById('comment')

    let info = document.getElementById('info-messages')
    let token = localStorage.getItem('token')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token},
        body: JSON.stringify({
            title: title.value,
            location: location.value,
            comment: comment.value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 201){
            frm.reset()
            info.parentElement.style.display='block';
            info.textContent = ""+data.data[0].message;
            return false;
        } else {
            info.parentElement.style.display='block';
            info.textContent = ""+data.error;
        }
        console.log(data)
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}