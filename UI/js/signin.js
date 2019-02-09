/* global document, sessionStorage, window, fetch */

const url = 'https://andelaireporterapp.herokuapp.com/auth/login';

function loginUser(event) {
  event.preventDefault();
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const info = document.getElementById('info-messages');
  const token = sessionStorage.getItem('token');

  fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer '+token },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 200) {
        window.location.replace('./index.html');
        sessionStorage.setItem('token', data.data[0].token);
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = data.error;
      }
    })
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

document.getElementById('login-form').addEventListener('submit', loginUser);
