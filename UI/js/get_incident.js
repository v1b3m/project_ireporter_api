
function getIncident(incident_id) {
    console.log("My id is "+ incident_id)
    const url = 'https://andelaireporterapp.herokuapp.com/api/v2/interventions/'.concat(incident_id)

    fetch (url, {
        method: 'GET',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': "Bearer " + token}
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 200) {
            flagId = document.getElementById('t-head')
            flagId.textContent = "Incident "+data.data[0].incident_id
            title = document.getElementById('title')
            title.textContent = data.data[0].title
            flagType = document.getElementById('type')
            flagType.textContent = data.data[0].type 
            createdOn = document.getElementById('created-on')
            createdOn.textContent = data.data[0].created_on
            createdBy = document.getElementById('author')
            createdBy.textContent = data.data[0].created_by
            coords = document.getElementById('coords')
            coords.textContent = data.data[0].location
            incStatus = document.getElementById('inc-status')
            incStatus.textContent = data.data[0].status
            comment = document.getElementById('comment')
            comment.textContent = data.data[0].comment
            images = document.getElementById('images')
            images.textContent = data.data[0].images
            videos = document.getElementById('videos')
            videos.textContent = data.data[0].videos
            
            console.log(data.data[0].status)
        }
    })
}