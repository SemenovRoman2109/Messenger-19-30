let url = `ws://${window.location.host}/chat`
const socket = new WebSocket(url)
const input = document.querySelector('input')
const button = document.querySelector('button')
let body = document.querySelector('body')

socket.onmessage = function(event){
    const data = JSON.parse(event.data)
    let text = document.createElement("h3")
    text.textContent = data.message
    body.append(text)
}

button.addEventListener('click', ()=>{
    socket.send(JSON.stringify({message: input.value}))
    input.value = ''
})