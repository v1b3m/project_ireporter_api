/* global document, sessionStorage, fetch, location, window */

// eslint-disable-next-line no-restricted-globals
const params = new URL(location.href).searchParams;
const incidentId = params.get('id');
const coords = params.get('location');
const incTitle = params.get('title');
const incComment = params.get('comment');
const frm = document.getElementById('edit-form');
const token = sessionStorage.getItem('token');
const info = document.getElementById('info-messages');

function fillForm() {
  const incId = document.getElementById('incident_id');
  incId.value = incidentId;
  const title = document.getElementById('title');
  title.value = incTitle;
  const location = document.getElementById('location');
  location.value = coords;
  const comment = document.getElementById('comment');
  comment.value = incComment;
}
fillForm();

function editLocation(id, coord) {
  const url = `https://andelaireporterapp.herokuapp.com/api/v2/red-flags/${id}/location`;
  fetch(url, {
    method: 'PATCH',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      location: coord,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status !== 201) {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    });
}

function editComment(id, comment) {
  const url = `https://andelaireporterapp.herokuapp.com/api/v2/red-flags/${id}/comment`;
  fetch(url, {
    method: 'PATCH',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      comment,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status !== 201) {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function editIncident(event) {
  event.preventDefault();
  const id = document.getElementById('incident_id').value.trim();
  const location = document.getElementById('location').value.trim();
  const comment = document.getElementById('comment').value.trim();
  editLocation(id, location);
  editComment(id, comment);
  info.parentElement.style.display = 'block';
  info.textContent = 'Successfully updated location and comment';
  await sleep(5000);
  window.location.replace('./index.html');
}

frm.addEventListener('submit', editIncident);
