/* global document, sessionStorage, fetch, window */
const token = sessionStorage.getItem('token');
const info = document.getElementById('info-messages');

// eslint-disable-next-line no-unused-vars
function getEditedIncidents(incidentType, newStatus) {
  const url = 'https://andelaireporterapp.herokuapp.com/api/v2/'.concat(incidentType);
  // const url = 'http://127.0.0.1:5000/api/v2/'.concat(incidentType);
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
          if (flag.status === newStatus) {
            const newRow = document.createElement('tr');
            const flagId = document.createElement('td');
            flagId.textContent = flag.incident_id;
            const title = document.createElement('td');
            title.innerHTML = `<a href="javascript:void(0);" onclick="getIncident(${flag.incident_id}); toggleModal();">${flag.title}</a>`;
            const flagType = document.createElement('td');
            flagType.textContent = flag.type;
            const createdOn = document.createElement('td');
            createdOn.textContent = flag.created_on;
            const createdBy = document.createElement('td');
            createdBy.textContent = flag.created_by;

            newRow.appendChild(flagId);
            newRow.appendChild(title);
            newRow.appendChild(flagType);
            newRow.appendChild(createdOn);
            newRow.appendChild(createdBy);

            tableBody.appendChild(newRow);
          } else {
            info.parentElement.style.display = 'block';
            info.textContent = `No new ${newStatus} incidents have been created`;
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
