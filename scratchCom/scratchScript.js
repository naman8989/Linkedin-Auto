
class listScrap{
    constructor(exp){
        // this.xhttp = new XMLHttpRequest();
        // this.xhttp.onload = ()=>{
        //     console.log("data on the road")
        // }
        console.log("started")
        try{
            this.experienceTab = exp
            this.scrapCompanyUrl(this.experienceTab)
        
        }catch(err){
            console.log("cannot find experience column ",err)
            return
        }
    }

    scrapCompanyUrl(exp) {
        this.compData = []
        try{
            this.expArray = Array.from(exp.children)
            this.expArray.forEach(element => {
                try{
                    this.companyName = element.children[0].children[1].children[0].children[0].children[1].children[0].innerText
                }catch(err){
                    this.companyName = "None"
                }
                try{
                    this.companyLocation = element.children[0].children[1].children[0].children[0].children[3].innerText
                }catch(err){
                    this.companyLocation = "None"
                }
                try{
                    this.companyUrl = element.children[0].children[0].children[0].getAttribute("href")
                }catch(err){
                    this.companyUrl = "None"
                }
                // console.log(this.companyName,this.companyLocation,this.companyUrl)
                this.pushCompanyData(this.companyName,this.companyLocation,this.companyUrl)
                
                this.setCompData(this.compData)
                
            });
        }catch(err){
            console.log("something went wrong while scrapping experiece tab " ,err)
        }
    }

    pushCompanyData(a,b,c){
        // this.xhttp.open("GET",`http://127.0.0.1:5000/companyData?cn=${a}&cl=${b}&cu=${c}`)
        // this.xhttp.send()
        this.compData.push([`${a}|${b}|${c}`])
    }

    setCompData(a){
        this.final = ""
        this.compData.forEach(ele=>{
            this.final = this.final.concat(ele,"||")
        })
        localStorage.setItem("companyData",this.final)
    }

}


interv = setInterval(()=>{
    expTab = document.getElementById("experience").parentElement.children[2].children[0]
    if (expTab != undefined) {
        scrap = new listScrap(expTab)
        console.log("in here")
        clearInterval(interv)
        
    }
},500)


function retComData(){
    return localStorage.getItem("companyData")
}