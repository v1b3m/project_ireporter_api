var token = sessionStorage.getItem('token')
let info = document.getElementById('info-messages')
var avatar;
var username;

function myIncidents(){
    const url = 'https://andelaireporterapp.herokuapp.com/user/incidents'
    let my_div = document.getElementById('my_items')

    fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    })
    .then((response) => response.json())
    .then((data) => {
        var table = ''
        if(data.length == 0){
            table = `<h1>Hello, ${username}</h1>
                        <h2>Your incidents will be displayed here</h2>
                        <h3>Go on to +Red Flags and +Interventions to create a new incident</h3>`
        }
        if (data) {
            console.log("hey")
            
            data.forEach(element => {
                table += 
                `
                <table class="table table-hover">
                    <tr>
                        <td width="70px">
                            <a href="profile.html">
                            <img src="${avatar}" /></a>
                        </td>
                        <td>
                            <a href="profile.html">
                            ${ username } </a>
                            added <a href='javascript:void(0);' onclick='getIncident(${element.incident_id}); toggleModal();'>
                            <b>${element.type} # ${element.incident_id }</b></a> on ${element.created_on}
                            <br>
                            ${ element.title }
                        </td>
                    </tr>
                </table>`;
            });                                            
            my_div.innerHTML = table;
        }
    })
    .catch((err) => console.log(err), info.textContent = 'An unknown error has occured! Please try again.')
}

function myStats(){
    const url = 'https://andelaireporterapp.herokuapp.com/user'
    let my_div = document.getElementById('my_items')

    fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    })
    .then((response) => response.json())
    .then((data) => {
        if (data) {
            avatar = data.gravatar
            avatar = avatar.concat(70)
            username = data.username
        }
    })
}

myStats()
myIncidents()

var modal = document.querySelector(".modal");
var closeButton = document.querySelector(".close-button");

function toggleModal() {
    modal.classList.toggle("show-modal");
}

closeButton.addEventListener("click", toggleModal);
