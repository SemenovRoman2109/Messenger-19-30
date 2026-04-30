const btnAddLink = document.querySelector('#add-link')
const listLinks = document.querySelector('#links-list')

btnAddLink.addEventListener('click', () => {
    const newLink = document.createElement('input')
    newLink.type = 'url'
    newLink.name = 'link'
    newLink.placeholder = 'enter link'
    listLinks.append(newLink)
})

