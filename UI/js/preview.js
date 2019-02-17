/* global document */

// eslint-disable-next-line no-unused-vars
function imagePreview(event) {
  const thumbnail = document.getElementById('thumbnail');
  thumbnail.style.display = 'block';
  thumbnail.src = URL.createObjectURL(event.target.files[0]);
}
