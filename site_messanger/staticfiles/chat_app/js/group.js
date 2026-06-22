const chatButton = document.querySelector("#open-group-modal")
const groupName = document.querySelector("#groupName")
const createGroup = document.querySelector('.create-group')

const groupModal = document.querySelector("#groupModal")
const createModal = document.querySelector("#createGroup")
const settingsModal = document.querySelector("#settingsGroup")

const closeModals = document.querySelectorAll(".close-modal")
const backModal = document.querySelector(".back-modal")
const nextModal = document.querySelector(".next-modal")

const allSelectFriends = document.querySelectorAll(".select-friend")

const settingsFriendsDiv = document.querySelector(".settings-friends-div")

const groupChats = document.querySelector('#group-chats')

chatButton.addEventListener('click', ()=>{
    createModal.style.display = 'flex'
    groupModal.style.display = 'flex'

    settingsModal.style.display = 'none'
})
closeModals.forEach(closeModal => {
    closeModal.addEventListener('click', ()=>{
        createModal.style.display = 'none'
        groupModal.style.display = 'none'

        settingsModal.style.display = 'none'
    })
})

backModal.addEventListener('click', ()=>{
    createModal.style.display = 'flex'
    groupModal.style.display = 'flex'

    settingsModal.style.display = 'none'
})

nextModal.addEventListener('click', ()=>{
    createModal.style.display = 'none'
    groupModal.style.display = 'flex'

    settingsModal.style.display = 'flex'
    
    settingsFriendsDiv.innerHTML = ""

    const selectedUsers = [...allSelectFriends].filter(cb => cb.checked)
    selectedUsers.forEach(selectFriend => {
        const name = selectFriend.previousElementSibling.textContent
        settingsFriendsDiv.innerHTML += `<h5>${name}</h5>`
    })
})

allSelectFriends.forEach(selectFriend => {
    selectFriend.addEventListener("input", () =>{
        const selectedUsers = [...allSelectFriends].filter(cb => cb.checked)
        
        const selectCount = document.querySelector("#selectCount")
        selectCount.textContent = `Вибрано: ${selectedUsers.length}`
    })

})


createGroup.addEventListener('click', async()=> {
    const selectedUsers = [...allSelectFriends].filter(cb => cb.checked)
    
    const data = {
        'name': groupName.value,
        'friends': []
    }
    
    selectedUsers.forEach(selectedUser => {
        data.friends.push(selectedUser.value)
    })

    const response = await fetch(
        '/chat/create/group/',
        {
            headers: {
                'X-CSRFToken' : csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            method: 'POST',
            body: JSON.stringify(data)
        }
    )
    const responseData = await response.json()
    createModal.style.display = 'none'
    groupModal.style.display = 'none'
    settingsModal.style.display = 'none'

    const newChat = document.createElement("button")
    newChat.dataset.id = responseData.chat_id
    newChat.textContent = responseData.name
    newChat.classList.add("chat-user-button")
    newChat.classList.add("chat")

    // openChat(responseData.chat_id)
    
    newChat.addEventListener("click", ()=>{
        openChat(responseData.chat_id)
    })

    groupChats.appendChild(newChat)
})
