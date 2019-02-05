const url = 'https://andelaireporterapp.herokuapp.com/api/v2/interventions'
var token = localStorage.getItem('token')
let info = document.getElementById('info-messages')

function getInterventions() {
    let tableBody = document.querySelector('#incidents-table > tbody')

    fetch (url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': "Bearer " + token}
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.status == 200) {
            for(let flag of data.data){
                newRow = document.createElement('tr')

                flagId = document.createElement('td')
                flagId.textContent = flag.incident_id
                title = document.createElement('td')
                title.textContent = flag.title
                flagType = document.createElement('td')
                flagType.textContent = flag.type 
                createdOn = document.createElement('td')
                createdOn.textContent = flag.created_on
                accept = document.createElement('td')
                accept.innerHTML = '<a href=""><i class="fa fa-check-square-o" aria-hidden="true"></i></a>'
                reject = document.createElement('td')
                reject.innerHTML = '<a href=""><i class="fa fa-ban" aria-hidden="true"></i></a>'

                newRow.appendChild(flagId)
                newRow.appendChild(title)
                newRow.appendChild(flagType)
                newRow.appendChild(createdOn)
                newRow.appendChild(accept)
                newRow.appendChild(reject)

                tableBody.appendChild(newRow)
            }
        } else {
            info.parentElement.style.display='block';
            info.textContent = ""+data.error;
        }
        console.log(data)
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}

getInterventions()
