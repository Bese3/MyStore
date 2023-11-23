$(document).ready(function (){
    let MyServer = "http://127.0.0.1:5000/";
    for (let i = 0; i < 3; i++){
        // console.log(MydescClass)
        $.ajax({
            type: 'GET',
            url: MyServer + "portfolios",
            success: (data) => {
                let MyNameClass = '.port-' + String(i + 1);
                let MydescClass = '.port-desc-' + String(i + 1);
                $(MyNameClass).text(data.name)
                $(MydescClass).text(data.description)
            }
        })
    }
    
})

$(document).ready(function (){
    let MyServer = "http://127.0.0.1:5000/";
    for (let i = 0; i < 3; i++){
        // console.log(MydescClass)
        $.ajax({
            type: 'GET',
            url: MyServer + "books",
            success: (data2) => {
                let MyBookClass = '.book-' + String(i + 1);
                let BookDescClass = '.book-desc-' + String(i + 1);
                $(MyBookClass).text(data2.name)
                $(BookDescClass).text(data2.author)
                // $(BookDescClass)
            }
        })
    }
    
})
