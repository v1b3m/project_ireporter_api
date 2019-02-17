/* global document, window, sessionStorage, fetch */

const token = sessionStorage.getItem('token');
const info = document.getElementById('info-messages');
let avatar = '';
let username = '';

function myIncidents() {
  const url = 'https://andelaireporterapp.herokuapp.com/user/incidents';
  // const url = 'http://127.0.0.1:5000/user/incidents';
  const myDiv = document.getElementById('my_items');

  fetch(url, {
    method: 'GET',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      let table = '';
      if (data.status === 401) {
        window.location.replace('./signin.html');
      }
      if (data.data.length === 0) {
        table = `<h1>Hello, ${username}</h1>
                  <h2>Your incidents will be displayed here</h2>
                  <h3>Go on to +Red Flags and +Interventions to create a new incident</h3>`;
      }
      if (data.data) {
        data.data.forEach((element) => {
          table
                += `
                <table class="table table-hover">
                    <tr>
                        <td width="70px">
                            <a href="profile.html">
                            <img src="${avatar}" /></a>
                        </td>
                        <td>
                            <a href="profile.html">
                            ${username} </a>
                            added <a href='javascript:void(0);' onclick='getIncident(${element.incident_id}); toggleModal();'>
                            <b>${element.type} # ${element.incident_id}</b></a> on ${element.created_on}
                            <br>
                            ${element.title}
                        </td>                        
                    </tr>                
                </table>`;
        });
        myDiv.innerHTML = table;
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    })
    // eslint-disable-next-line no-console
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

function myStats() {
  const url = 'https://andelaireporterapp.herokuapp.com/user';
  // const url = 'http://127.0.0.1:5000/user';

  fetch(url, {
    method: 'GET',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      if (data) {
        if (data.status === 401) {
          window.location.replace('./signin.html');
        }
        avatar = data.data.gravatar;
        avatar = avatar.concat(70);
        // eslint-disable-next-line prefer-destructuring
        username = data.data.username;
      }
    });
}

myStats();
myIncidents();

const modal = document.querySelector('.modal');
const closeButton = document.querySelector('.close-button');

function toggleModal() {
  modal.classList.toggle('show-modal');
}

closeButton.addEventListener('click', toggleModal);
