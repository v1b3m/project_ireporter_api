/* global document, sessionStorage, window, fetch */

const signOut = document.getElementById('logout');
const url = 'https://andelaireporterapp.herokuapp.com/auth/logout';

function logoutUser() {
  const info = document.getElementById('info-messages');
  const token = sessionStorage.getItem('token');

  fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 200) {
        window.location.replace('./signin.html');
        sessionStorage.clear();
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = data.error;
      }
    })
    // eslint-disable-next-line no-console
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

signOut.addEventListener('click', logoutUser);
