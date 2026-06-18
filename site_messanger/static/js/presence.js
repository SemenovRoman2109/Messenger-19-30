const url = `ws://${window.location.host}/presence/`;
const presenceSocket = new WebSocket(url)

presenceSocket.onmessage = (event) =>{
    const data = JSON.parse(event.data)
    
    const userMarkers = document.querySelectorAll(".online-marker")
    if (data.type == 'get_online'){
        userMarkers.forEach(marker => {
            if(marker.dataset.id in data.online_users){
                marker.classList.add('active-marker')
            }
            else{
                marker.classList.remove('active-marker')
            }
        })
    }else if (data.type == 'send_message'){
        console.log(data)
        document.querySelectorAll('.chat-user-button').forEach(btn => {
            console.log("btn");
            
            if (btn.dataset.id != chatId && btn.dataset.id == data.chat_id){
                console.log("create");
                
                const unread = btn.querySelector('.unread')
                if(unread){
                    unread.textContent = Number(unread.textContent) + 1
                }else{
                    const newUnread = document.createElement('h6')
                    newUnread.classList.add('unread')
                    newUnread.textContent = 1
                    btn.append(newUnread)
                }
                renderCountUnreadedMessages()
            }
        })
    }else{
       userMarkers.forEach(marker =>{
        if (marker.dataset.id == data.user_id){
            if(data.status){
                marker.classList.add('active-marker')
            }
            else{
                marker.classList.remove('active-marker')
            }
        }
        })
        try{
            updateGroupUsers(data.user_id, data.status)
        }
        catch{
            
        }
    }
}