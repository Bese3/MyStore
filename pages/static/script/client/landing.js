$(document).ready(function (){
    let MyServer = "https://www.besufikadyilma.tech/";
    for (let i = 0; i < 3; i++){
        // console.log(MydescClass)
        $.ajax({
            type: 'GET',
            url: MyServer + "all",
            success: (data) => {
                // console.log(data)
                let MyNameClass = '.port-' + String(i + 1);
                let MydescClass = '.port-desc-' + String(i + 1);
                // $(MyNameClass).text(data[0].name)
                $(MydescClass).text(data[0].description)
                $(MydescClass).css("display", "flex");

                let MyBookClass = '.book-' + String(i + 1);
                let BookDescClass = '.book-desc-' + String(i + 1);
                $(MyBookClass).text(data[1].name)
                $(BookDescClass).text(data[1].author)
                $(BookDescClass).css("display", "flex");
                $(BookDescClass).css("justify-content", "end");
                $(BookDescClass).css("height", "120px");
                $(BookDescClass).css("position", "relative");
                $(BookDescClass).css("align-items", "end");
            }
        })
    }
    
})
