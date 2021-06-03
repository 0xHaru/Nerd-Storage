// Global Variables
let flag = 0

// Functions
function setupEditBtn() {
    document.querySelector('#edit-button').addEventListener('click', (event) => {
        toggleBtnVisibility()
    })
}

function toggleBtnVisibility() {
    const visibility = flag ? 'hidden' : 'visible'
    flag = !flag

    document.querySelectorAll('.delete').forEach((button) => {
        button.style.visibility = visibility
    })

    document.querySelectorAll('.update').forEach((button) => {
        button.style.visibility = visibility
    })
}

function setupUpdateBtn() {
    document.querySelectorAll('.update').forEach((button) => {
        button.addEventListener('click', (event) => {
            updateDialog(button)
        })
    })
}

function updateDialog(button) {
    const resourceName = button.name

    const form = document.querySelector('#update-dialog')
    const originalName = document.querySelector('#update-dialog > input:nth-child(3)')
    const updatedName = document.querySelector('#update-dialog > input:nth-child(7)')

    updatedName.value = resourceName
    originalName.value = resourceName

    form.style.visibility = 'visible'

    $('#update-dialog').dialog({
        resizable: false,
        height: 'auto',
        width: 400,
        modal: true,
        buttons: {
            Update: function () {
                $(this).dialog('close')
                $('#update-dialog').submit()
            },
            Cancel: function () {
                $(this).dialog('close')
            },
        },
    })
}

function setupDeleteBtn() {
    document.querySelectorAll('.delete').forEach((button) => {
        button.addEventListener('click', (event) => {
            deleteDialog(button.name)
        })
    })
}

function deleteDialog(name) {
    const resourceName = name

    const deleteDialog = document.querySelector('#delete-dialog')
    deleteDialog.innerHTML = `Are you sure you want to delete ${resourceName}?`

    $('#delete-dialog').dialog({
        resizable: false,
        height: 'auto',
        width: 400,
        modal: true,
        buttons: {
            Delete: function () {
                $(this).dialog('close')
                deleteResource(resourceName)
            },
            Cancel: function () {
                $(this).dialog('close')
            },
        },
    })
}

function deleteResource(name) {
    const path = window.location.pathname
    const resource = `${path}/${name}`

    fetch(resource, { method: 'DELETE' }).then(() => location.reload())
}

// Execution
setupDeleteBtn()
setupUpdateBtn()
setupEditBtn()
