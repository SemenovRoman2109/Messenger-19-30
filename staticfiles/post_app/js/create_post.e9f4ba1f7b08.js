const btnAddLink = document.querySelector('#add-link')
const listLinks = document.querySelector('#links-list')

function getCSRFToken(){
    const meta = document.querySelector("meta[name='csrfToken']")
    return meta.content
}

btnAddLink.addEventListener('click', () => {
    const newLink = document.createElement('input')
    newLink.type = 'url'
    newLink.name = 'link'
    newLink.placeholder = 'enter link'
    listLinks.append(newLink)
})

const formPost = document.querySelector('form')
formPost.addEventListener("submit", async (event) => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const response = await fetch(formPost.action,{
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Request-With': 'XMLHttpRequest'
        }
    } )
    const data = await response.json()
    console.log(data)
})