let MyServer = "http://127.0.0.1:5001/api/v1/"
$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5002/session',
        success: (json) => {
            console.log(json.userinfo)
            $.ajax({
                type: 'GET',
                url: MyServer + 'users',
                success: (json2) => {
                    let Available = false;
                    let user_id;
                    for (let i = 0; i < json2.length; i++){
                        if (json2[i].email === json.userinfo.email) {
                            Available = true;
                            if (json2[i].first_name != undefined && json2[i].last_name != undefined){
                               $('.owner').text('Owner: ' + json2[i].first_name + " " + json2[i].last_name);
                            }
                            user_id = json2[i].id;
                        }
                    }
                    if (Available === false){
                        $.ajax({
                            type: 'POST',
                            url: MyServer + 'user',
                            contentType: "application/json",
                            data: JSON.stringify({"email": json.userinfo.email, "password": "12345678"}),
                            success: (json3) => {
                                if (json.first_name != undefined && json.last_name != undefined){
                                   $('.owner').text('Owner: ' + json.first_name + " " + json.last_name);
                                }
                               user_id = json.id;
                            }
                        })
                    }

                }
            })
        }
    })
})