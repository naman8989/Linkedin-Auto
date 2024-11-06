companyName = "none"
companyOriginalUrl = "none"

interv = setInterval(()=>{
    try{
        bar = document.getElementsByClassName("ph5 pb5")[0].children[0].children[1].children[0].children[0].innerText
    }catch(err){
        bar == undefined
    }
    if (bar != undefined){
        clearInterval(interv)
        companyOriginalUrl = location.href
        localStorage.setItem("compData",`${bar}|${companyOriginalUrl}`)
    }

},500)