const editBtns = document.querySelectorAll('.edit')
const selectAvatar = document.querySelector('#select-avatar')
const fileInput = document.querySelector('#fileInput')

editBtns.forEach(btn => {
    btn.addEventListener('click', ()=> {
        btn.closest('form').querySelectorAll('.visible-save').forEach(el=>{
            el.style.display = 'none'
        })
        btn.closest('form').querySelectorAll('.visible-edit').forEach(el=>{
            el.style.display = 'flex'
        })
        btn.closest('form').querySelectorAll('.visible-dissable').forEach(el=>{
            el.classList.remove("visible-dissable")
        })
    })
})


selectAvatar.addEventListener("click", () =>{
    fileInput.click()
})