function getCSRFToken(){
    const meta = document.querySelector("meta[name='csrfToken']")
    return meta.content
}

const containerRegistration = document.querySelector("#containerRegistration")
const containerLogin = document.querySelector("#containerLogin")
const containerConfirmEmail = document.querySelector("#containerConfirmEmail")

const registerErrorContainer = document.querySelector("#registerErrorContainer")
const loginErrorContainer = document.querySelector("#loginErrorContainer")

const toRegistration = document.querySelector("#toRegistration")
const toLogin = document.querySelector("#toLogin")

toLogin.addEventListener('click', ()=>{
    containerRegistration.style.display = "none"
    containerLogin.style.display = 'block'
})

toRegistration.addEventListener('click', ()=>{
    containerLogin.style.display = "none"
    containerRegistration.style.display = 'block'
})

const formLogin = document.querySelector("#formLogin")
const formRegister = document.querySelector("#formRegister")

formRegister.addEventListener('submit', async function(event){
    event.preventDefault()
    const formData = new FormData(event.target)
    const response = await fetch(formRegister.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    if (data.success == true) {
        formRegister.reset()
        containerRegistration.style.display = "none"
        containerLogin.style.display = 'block'
    } else {
        registerErrorContainer.innerHTML = ''
        for (const key in data.errors) {
            const errors = data.errors[key];
            errors.forEach(error => {
                const errorElement = document.createElement('p')
                errorElement.textContent = error.message
                registerErrorContainer.append(errorElement)
            });
        }
    }
})

formLogin.addEventListener('submit', async function(event){
    event.preventDefault()
    const formData = new FormData(event.target)
    const response = await fetch(formLogin.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    if (data.success == true) {
        formLogin.reset()
        window.location.href = '/'
    } else {
        loginErrorContainer.innerHTML = ''
        for (const key in data.errors) {
            const errors = data.errors[key];
            errors.forEach(error => {
                const errorElement = document.createElement('p')
                errorElement.textContent = error.message
                loginErrorContainer.append(errorElement)
            });
        }
    }
})