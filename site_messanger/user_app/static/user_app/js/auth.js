function getCSRFToken(){
    const meta = document.querySelector("meta[name='csrf_token']")
    return meta.content
}

console.log(getCSRFToken())

// (js) В селекторі можна вказати значення атрибуту -> "input[type='text']"