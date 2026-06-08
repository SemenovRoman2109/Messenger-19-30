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
    }
}