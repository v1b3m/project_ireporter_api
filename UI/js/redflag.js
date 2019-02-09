/* global document, sessionStorage, fetch */

const frm = document.getElementById('red-flag-form');

const url = 'https://andelaireporterapp.herokuapp.com/api/v2/red-flags'

function createRedflag(event) {
  event.preventDefault();
  const title = document.getElementById('title');
  const location = document.getElementById('location');
  const comment = document.getElementById('comment');

  const info = document.getElementById('info-messages');
  const token = sessionStorage.getItem('token');

  fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer '+ token },
    body: JSON.stringify({
      title: title.value,
      location: location.value,
      comment: comment.value,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 201) {
        frm.reset();
        info.parentElement.style.display = 'block';
        info.textContent = ''+data.data[0].message;
        return false;
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = ''+data.error;
      }
    })
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

frm.addEventListener('submit', createRedflag)