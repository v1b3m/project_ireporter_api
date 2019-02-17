/* global document, sessionStorage, window, fetch */

const url = 'https://andelaireporterapp.herokuapp.com/auth/login';
// const url = 'http://127.0.0.1:5000/auth/login';

function loginUser(event) {
  event.preventDefault();
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const info = document.getElementById('info-messages');
  const token = sessionStorage.getItem('token');

  fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 200) {
        sessionStorage.setItem('token', data.data[0].token);
        if (document.getElementById('is_admin').checked) {
          window.location.replace('./admin.html');
        } else {
          window.location.replace('./index.html');
        }
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = data.error;
      }
    })
    // eslint-disable-next-line no-console
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

document.getElementById('login-form').addEventListener('submit', loginUser);
