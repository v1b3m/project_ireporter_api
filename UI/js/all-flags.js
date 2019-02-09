/* global document, sessionStorage, fetch */

const token = sessionStorage.getItem('token');
const info = document.getElementById('info-messages');
const modal = document.querySelector('.modal');
const closeButton = document.querySelector('.close-button');

// eslint-disable-next-line no-unused-vars
function getIncidents(incidentType) {
  const url = 'https://andelaireporterapp.herokuapp.com/api/v2/'.concat(incidentType);
  const tableBody = document.querySelector('#incidents-table > tbody');

  fetch(url, {
    method: 'GET',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 200) {
        data.data.forEach((flag) => {
        // })
        // for(const flag of data.data) {
          const newRow = document.createElement('tr');
          const flagId = document.createElement('td');
          flagId.textContent = flag.incident_id;
          const title = document.createElement('td');
          title.innerHTML = '<a href="javascript:void(0);" onclick="getIncident('+flag.incident_id+'); toggleModal();">'+flag.title+'</a>';
          const flagType = document.createElement('td');
          flagType.textContent = flag.type;
          const createdOn = document.createElement('td');
          createdOn.textContent = flag.created_on;
          const accept = document.createElement('td');
          accept.innerHTML = '<a href=""><i class="fa fa-check-square-o" aria-hidden="true"></i></a>';
          const reject = document.createElement('td');
          reject.innerHTML = '<a href=""><i class="fa fa-ban" aria-hidden="true"></i></a>';

          newRow.appendChild(flagId);
          newRow.appendChild(title);
          newRow.appendChild(flagType);
          newRow.appendChild(createdOn);
          newRow.appendChild(accept);
          newRow.appendChild(reject);

          tableBody.appendChild(newRow);
        });
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    })
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}


function toggleModal() {
  modal.classList.toggle('show-modal');
}

closeButton.addEventListener('click', toggleModal);
