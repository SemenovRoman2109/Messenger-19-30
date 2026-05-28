const chatBtns = document.querySelectorAll(".chat")
const chat = document.querySelector("#chat")
const notSelectContainer = document.querySelector("#not-select")
let chatSocket;
const friendDivs = document.querySelectorAll(".friend-div")
const csrfToken = document.querySelector("meta[name='csrfToken']").content
const messages = document.querySelector('#messages')
const loadLine = document.querySelector("#load-message-line")
let pageNumber = 1

async function loadMessages(chatId){
    const response = await fetch(
        `/chat/${chatId}/getMessages/?page=${pageNumber}`,
        {headers: {'X-Requested-With': 'XMLHttpRequest'}}
    )
    const data = await response.json()
    console.log(data);
    
    if (data.success){
        data.messages.forEach((message)=>{
            createMessage(message.sender, message.text, message.datetime, false)
        })
    }
}

function createMessage(sender, text, dateTime, isNew = true){
    const newMessage = document.createElement('div')
    newMessage.classList.add('message')
    newMessage.innerHTML = `
        <h5>${sender}</h5>
        <h3>${text}</h3>
        <h6>${dateTime}</h6>
    `
    if(isNew){
        messages.appendChild(newMessage)
    }
    else{
        messages.insertBefore(newMessage, loadLine.nextElementSibling)
    }
}

function openChat(chatId){
    notSelectContainer.style.display = "none"
    chat.style.display = "flex"
    messages.querySelectorAll(".message").forEach((msg) =>{
        msg.remove()
    })
    pageNumber = 1
    loadMessages(chatId)
    if (chatSocket){
        chatSocket.close()
    }
    let url = `ws://${window.location.host}/chat/${chatId}`;
    chatSocket = new WebSocket(url)
    chatSocket.onmessage = (event)=>{
        const data = JSON.parse(event.data)
        console.log(data.message);
        
        if (data.message){
            createMessage(data.message.sender, data.message.text, data.message.datetime)
        }
    }
}

chatBtns.forEach(btn => {
    btn.addEventListener('click', ()=>{
        openChat(btn.dataset.id)
    })
})

const sendMsg = document.querySelector("#send-msg")
const msgInput = document.querySelector("#msg-input")

sendMsg.addEventListener("click", ()=>{
    chatSocket.send(
        JSON.stringify({
            "msg": msgInput.value
        })
    )
    msgInput.value = ''
})

friendDivs.forEach(div => {
    div.addEventListener('click', async ()=>{
        const response = await fetch('/chat/create/', {
            method: "POST",
            headers: {
                'X-CSRFToken' : csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }, 
            body: JSON.stringify({
                friend_id: div.dataset.id
            })
        })
        const data = await response.json()
        if (data.is_new){
            const newChat = document.createElement('div')
            newChat.classList.add('chat')
            newChat.innerHTML = `<h3>${data.friend_email}</h3>`
            newChat.dataset.id = data.chat_id
            newChat.addEventListener('click', ()=>{
                openChat(data.chat_id)
            })
            document.querySelector('#indiv-chats').append(newChat)
        }
        openChat(data.chat_id)
    })
})