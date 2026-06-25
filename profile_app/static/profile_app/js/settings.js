const editBtns = document.querySelectorAll('.edit')
const cancelBtns = document.querySelectorAll('.cancel')
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

cancelBtns.forEach(btn => {
    btn.addEventListener('click', ()=> {
        btn.closest('form').querySelectorAll('.visible-save').forEach(el=>{
            el.style.display = 'flex'
        })
        btn.closest('form').querySelectorAll('.visible-edit').forEach(el=>{
            el.style.display = 'none'
        })
        btn.closest('form').querySelectorAll('.dissable').forEach(el=>{
            el.classList.add("visible-dissable")
        })
    })
})

// {{ змінна|date:"Y-m-d" }} - фільтр date в html, відображає дату у вказаному форматі. ( замість тире може бути будь-що )

selectAvatar.addEventListener("click", () =>{
    fileInput.click()
})