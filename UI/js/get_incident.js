/* global document, window, fetch */

// eslint-disable-next-line no-unused-vars
function getIncident(incidentId) {
  const url = 'https://andelaireporterapp.herokuapp.com/api/v2/interventions/'.concat(incidentId);

  fetch(url, {
    method: 'GET',
    mode: 'cors',
    // eslint-disable-next-line no-undef
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 401) {
        window.location.replace('./signin.html');
      }
      if (data.status === 200) {
        const flagId = document.getElementById('t-head');
        flagId.textContent = `Incident #${data.data[0].incident_id}`;
        const editIncident = document.getElementById('edit');
        if (editIncident) {
          editIncident.innerHTML = `<a href="edit.html?
          &id=${data.data[0].incident_id}
          &location=${data.data[0].location}
          &comment=${data.data[0].comment}
          &title=${data.data[0].title}">Edit this incident</a>`;
        }
        const title = document.getElementById('title');
        title.textContent = data.data[0].title;
        const flagType = document.getElementById('type');
        flagType.textContent = data.data[0].type;
        const createdOn = document.getElementById('created-on');
        createdOn.textContent = data.data[0].created_on;
        const createdBy = document.getElementById('author');
        createdBy.textContent = data.data[0].created_by;
        const coords = document.getElementById('coords');
        coords.textContent = data.data[0].location;
        const incStatus = document.getElementById('inc-status');
        incStatus.textContent = data.data[0].status;
        const comment = document.getElementById('comment');
        comment.textContent = data.data[0].comment;
        const images = document.getElementById('images');
        images.innerHTML = `<a href="./viewfile.html?
          &filename=${data.data[0].images}">${data.data[0].images}</a>`;
        const videos = document.getElementById('videos');
        videos.innerHTML = `<a href="./getvideo.html?
          &filename=${data.data[0].videos}">${data.data[0].videos}</a>`;
      }
    });
}
