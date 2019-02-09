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
        console.log(data)
        if (data) {
            console.log("hey")
            var table = ''
            data.forEach(element => {
                table += 
                `
                <table class="table table-hover">
                    <tr>
                        <td width="70px">
                            <a href="#">
                            <img src="${avatar}" /></a>
                        </td>
                        <td>
                            <a href="#">
                            ${ username } </a>
                            added <b>${element.type} # ${element.incident_id }</b> on ${element.created_on}
                            <br>
                            ${ element.title }
                        </td>
                    </tr>
                </table>`;
            });                                            
            my_div.innerHTML = table;
        }
    })
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
        console.log(data)
        if (data) {
            avatar = data.gravatar
            avatar = avatar.concat('70')
            username = data.username
        }
    })
}

myStats()
myIncidents()
