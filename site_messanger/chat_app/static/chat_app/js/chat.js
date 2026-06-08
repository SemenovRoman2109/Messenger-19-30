const chatBtns = document.querySelectorAll(".chat")
const chat = document.querySelector("#chat")
const notSelectContainer = document.querySelector("#not-select")
let chatSocket;
const friendDivs = document.querySelectorAll(".friend-div")
const csrfToken = document.querySelector("meta[name='csrfToken']").content
const messages = document.querySelector('#messages')
const loadLine = document.querySelector("#load-message-line")
let pageNumber = 1
let chatId = null
let observer = null

async function loadMessages(){
    const response = await fetch(
        `/chat/${chatId}/getMessages/?page=${pageNumber}`,
        {headers: {'X-Requested-With': 'XMLHttpRequest'}}
    )
    const data = await response.json()
    console.log(data)
    
    if (data.success){
        data.messages.forEach((message)=>{
            createMessage(message.sender, message.text, message.date, message.time, message.images,  false)
        })
        createDateMessage()
    }else if (observer != null){
        observer.disconnect()
    }
}

function createMessage(sender, text, date, time, images, isNew = true){
    const newMessage = document.createElement('div')
    newMessage.classList.add('message')
    newMessage.innerHTML = `
        <h5>${sender}</h5>
        <h3>${text}</h3>
        <h6>${time}</h6>
    `
    if (images){
        images.forEach(imageUrl =>{
            const newImage = document.createElement("img") 
            newImage.classList.add('chat-image')
            newImage.src = imageUrl
            newMessage.append(newImage)
        })
    }
    newMessage.dataset.date = date
    if(isNew){
        messages.appendChild(newMessage)
    }
    else{
        messages.insertBefore(newMessage, loadLine.nextElementSibling)
    }
}

function openChat(id){
    notSelectContainer.style.display = "none"
    chat.style.display = "flex"
    messages.querySelectorAll(".message").forEach((msg) =>{
        msg.remove()
    })
    pageNumber = 1
    chatId = id
    loadMessages().then(()=>{
        messages.scrollTop = messages.scrollHeight
        startObserveMessage()
    })
    if (chatSocket){
        chatSocket.close()
    }
    let url = `ws://${window.location.host}/chat/${id}`;
    chatSocket = new WebSocket(url)
    chatSocket.onmessage = (event)=>{
        const data = JSON.parse(event.data)
        
        if (data.message){
            createMessage(data.message.sender, data.message.text, data.message.date, data.message.time, data.message.images)
            messages.scrollTop = messages.scrollHeight
            createDateMessage()
        }
    }
}

async function startObserveMessage(){
    observer = new IntersectionObserver(async (entries) => {
        if (entries[0].isIntersecting){
            pageNumber += 1
            await loadMessages()
        }
    }, {rootMargin: "70px"})
    observer.observe(loadLine)
}

chatBtns.forEach(btn => {
    btn.addEventListener('click', ()=>{
        openChat(btn.dataset.id)
    })
})

const sendMsg = document.querySelector("#send-msg")
const msgInput = document.querySelector("#msg-input")
const msgImageInput = document.querySelector("#message-files")

sendMsg.addEventListener("click", async ()=>{
    if (msgImageInput.files.length > 0){
        const formData = new FormData()
        formData.append("text", msgInput.value)
        formData.append("chat_id", chatId )

        const files = Array.from(msgImageInput.files)
        files.forEach(file =>{
            formData.append("image", file) 
        })

        const response = await fetch('/chat/create/message/', {
            method: "POST",
            headers: {
                'X-CSRFToken' : csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
    }else{
        chatSocket.send(
            JSON.stringify({
                "msg": msgInput.value
            })
        )
    }
    msgInput.value = ''
    msgImageInput.value = ''
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
            const newChat = document.createElement('button')
            newChat.classList.add('chat')
            newChat.classList.add("chat-user-button")
            newChat.textContent = data.friend_email
            newChat.dataset.id = data.chat_id
            newChat.addEventListener('click', ()=>{
                openChat(data.chat_id)
            })
            document.querySelector('#indiv-chats').append(newChat)
        }
        openChat(data.chat_id)
    })
})

function createDateMessage(){
    const messageDates = document.querySelectorAll('.message-date')
    messageDates.forEach(date => {
        date.remove()
    })
    
    const messageList = document.querySelectorAll('.message')
    let previousMessageDate = null
    messageList.forEach(message => {
        if(previousMessageDate != message.dataset.date){
            const dateTitle = document.createElement('h4')
            dateTitle.classList.add('message-date')
            dateTitle.textContent = message.dataset.date
            messages.insertBefore(dateTitle, message)
        }
        previousMessageDate = message.dataset.date
    })
}