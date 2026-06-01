const chatButton = document.querySelector("#open-group-modal")

const groupModal = document.querySelector("#groupModal")
const createModal = document.querySelector("#createGroup")
const settingsModal = document.querySelector("#settingsGroup")

const closeModals = document.querySelectorAll(".close-modal")
const backModal = document.querySelector(".back-modal")
const nextModal = document.querySelector(".next-modal")

const allSelectFriends = document.querySelectorAll(".select-friend")

const settingsFriendsDiv = document.querySelector(".settings-friends-div")


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