/* global document */

// eslint-disable-next-line func-names
document.onreadystatechange = function () {
  const state = document.readyState;
  if (state === 'complete') {
    document.getElementById('interactive');
    document.getElementById('load').style.visibility = 'hidden';
  }
};
