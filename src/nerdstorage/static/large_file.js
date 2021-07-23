const flow = new Flow({
    target: '/large-file/upload',
    simultaneousUploads: 5,
    chunkSize: 100 * 1024 * 1024,
    testChunks: true,
    singleFile: true,
})

flow.assignBrowse(document.querySelector('#browseButton'))

flow.on('fileAdded', function (file, event) {
    document.querySelector('#filename-label').innerHTML = file.name
})

flow.on('fileSuccess', function (file, message) {
    window.location.href = '/index'
})

flow.on('fileError', function (file, message) {
    const span = document.createElement('span')
    span.className = 'centered margin-y'
    span.innerHTML = `<h4>Error: ${file.name} upload failed</h4>`
    document.body.appendChild(span)
})

document.getElementById('submitButton').addEventListener('click', function () {
    const span = document.createElement('span')
    span.className = 'centered margin-y'
    span.innerHTML = `<h4>Uploading...</h4>`
    document.body.appendChild(span)

    flow.upload()
})
