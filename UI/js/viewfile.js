/* global document, location */
// eslint-disable-next-line no-restricted-globals
const params = new URL(location.href).searchParams;
const filename = params.get('filename');
const url = `https://andelaireporterapp.herokuapp.com/getimage/${filename}`;
const display = document.getElementById('image-preview');
display.src = url;
