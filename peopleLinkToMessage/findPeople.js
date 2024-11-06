tem = document.getElementsByClassName("artdeco-carousel ember-view org-people__carousel-container")[0].children[1].children[0].children[2].children[0].children[0].children[0].children
temp = Array.from(tem)
column = []
temp.forEach((element,index) => {
    if (index != 0){
        column.push(element.children[0].children[1].innerText)
        console.log(element.children[0].children[1].innerText)
    }
});
return JSON.stringify(column)


// last iteration 520