/* global document */

// eslint-disable-next-line no-unused-vars
function makeResponsive() {
  const i = document.getElementById('mynavbar');
  if (i.className === 'navbar') {
    i.className += ' responsive';
  } else {
    i.className = 'navbar';
  }
}
