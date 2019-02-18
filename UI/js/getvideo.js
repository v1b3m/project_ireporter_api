/* global document, location */
// eslint-disable-next-line no-restricted-globals
const params = new URL(location.href).searchParams;
const filename = params.get('filename');
const url = `http://127.0.0.1:5000/getvideo/${filename}`;
const video = document.getElementById('video');
const source = document.createElement('source');

source.setAttribute('src', url);

video.appendChild(source);
video.play();
