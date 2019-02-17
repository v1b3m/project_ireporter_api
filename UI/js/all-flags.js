/* global document, sessionStorage, window, fetch */

const token = sessionStorage.getItem('token');
const info = document.getElementById('info-messages');
const modal = document.querySelector('.modal');
const closeButton = document.querySelector('.close-button');

// eslint-disable-next-line no-unused-vars
function editStatus(id, status) {
  // const url = `https://andelaireporterapp.herokuapp.com/api/v2/red-flags/${id}/status`;
  const url = `http://127.0.0:5000/api/v2/red-flags/${id}/status`;
  fetch(url, {
    method: 'PATCH',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      status,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 401) {
        window.location.replace('./signin.html');
      }
      if (data.status !== 201) {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    });
}


// eslint-disable-next-line no-unused-vars
function getIncidents(incidentType) {
  // const url = 'https://andelaireporterapp.herokuapp.com/api/v2/'.concat(incidentType);
  const url = 'http://127.0.0.1:5000/api/v2/'.concat(incidentType);
  const tableBody = document.querySelector('#incidents-table > tbody');

  fetch(url, {
    method: 'GET',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 401) {
        window.location.replace('./signin.html');
      }
      if (data.status === 200) {
        data.data.forEach((flag) => {
          if (flag.status === 'under investigation') {
            const newRow = document.createElement('tr');
            const flagId = document.createElement('td');
            flagId.textContent = flag.incident_id;
            const title = document.createElement('td');
            title.innerHTML = `<a href="javascript:void(0);" onclick="getIncident(${flag.incident_id}); toggleModal();">${flag.title}</a>`;
            const flagType = document.createElement('td');
            flagType.textContent = flag.type;
            const createdOn = document.createElement('td');
            createdOn.textContent = flag.created_on;
            const accept = document.createElement('td');
            accept.innerHTML = `<a href="javascript:void(0);" onclick="editStatus(${flag.incident_id}, 'resolved');"><i class="fa fa-check-square-o" aria-hidden="true"></i></a>`;
            const reject = document.createElement('td');
            reject.innerHTML = `<a href="javascript:void(0);" onclick="editStatus(${flag.incident_id}, 'rejected');"><i class="fa fa-ban" aria-hidden="true"></i></a>`;

            newRow.appendChild(flagId);
            newRow.appendChild(title);
            newRow.appendChild(flagType);
            newRow.appendChild(createdOn);
            newRow.appendChild(accept);
            newRow.appendChild(reject);

            tableBody.appendChild(newRow);
          } else {
            info.parentElement.style.display = 'block';
            info.textContent = 'No new incidents have been created';
          }
        });
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    })
    // eslint-disable-next-line no-console
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}


function toggleModal() {
  modal.classList.toggle('show-modal');
}

closeButton.addEventListener('click', toggleModal);
