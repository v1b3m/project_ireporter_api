/* global document, sessionStorage, window, fetch */
const url = 'http://127.0.0.1:5000/auth/register';

function registerNewUser(event) {
  event.preventDefault();
  const firstname = document.getElementById('firstname');
  const lastname = document.getElementById('lastname');
  const othernames = document.getElementById('othernames');
  const username = document.getElementById('username');
  const email = document.getElementById('email');
  const phoneNumber = document.getElementById('phone_number');
  const password = document.getElementById('password');

  const info = document.getElementById('info-messages');
  const token = sessionStorage.getItem('token');

  fetch(url, {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      username: username.value,
      email: email.value,
      phone_number: phoneNumber.value,
      password: password.value,
      othernames: othernames.value,
      lastname: lastname.value,
      firstname: firstname.value,
    }),
  })
    .then(response => response.json())
    .then((data) => {
      if (data.status === 201) {
        window.location.replace('./signin.html');
      } else {
        info.parentElement.style.display = 'block';
        info.textContent = `${data.error}`;
      }
    })
    // eslint-disable-next-line no-console
    .catch(err => console.log(err), info.textContent = 'An unknown error has occured! Please try again.');
}

document.getElementById('registration-form').addEventListener('submit', registerNewUser);
