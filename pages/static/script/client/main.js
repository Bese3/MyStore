let MyServer = "http://52.201.220.122:5001/api/v1/"
$(document).ready(function () {
    let user_id;
    $.ajax({
        type: 'GET',
        url: 'http://52.201.220.122:5002/session',
        success: (json) => {
            // console.log(json.userinfo)
            $.ajax({
                type: 'GET',
                url: MyServer + 'users',
                success: (json2) => {
                    let users = json2;
                    let Available = false;
                    for (let i = 0; i < json2.length; i++){
                        if (json2[i].email === json.email) {
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
                            data: JSON.stringify({"email": json.email, "password": "12345678"}),
                            success: (json3) => {
                                if (json.first_name != undefined && json.last_name != undefined){
                                   $('.owner').text('Owner: ' + json.first_name + " " + json.last_name);
                                }
                               user_id = json.id;
                            }
                        })
                    }
                    $.ajax({
                        type: 'GET',
                        url: MyServer + user_id + "/portfolios",
                        success: (json) => {
                            // console.log(json)
                            for (let i = 0; i < json.length; i++){
                                $('.port-list').append('<li data-id=' + json[i].id +  '><input type="radio" name="port" value=' + json[i].id + '><a href=' + json[i].link + ' target="_blank">'
                                + json[i].name + '</a></li>')
                            }
                            $.ajax({
                                type: 'GET',
                                url: MyServer + user_id + "/books",
                                success: (json) => {
                                    // console.log(json)
                                    for (let i = 0; i < json.length; i++){
                                        $('.book-list').append('<li data-id=' + json[i].id +  '><input type="radio" name="book" value=' + json[i].id + '><a href=' + json[i].link + ' target="_blank">'
                                        + json[i].name + '</a></li>')
                                    }
                                    $.ajax({
                                        type: 'GET',
                                        url: MyServer + user_id + "/movies",
                                        success: (json) => {
                                            // console.log(json)
                                            for (let i = 0; i < json.length; i++){
                                                $('.movie-list').append('<li data-id=' + json[i].id +  '><input type="radio" name="movie" value=' + json[i].id + '><a href=' + json[i].link + ' target="_blank">'
                                                + json[i].name + '</a></li>')
                                            }
                                            $.ajax({
                                                type: 'GET',
                                                url: MyServer + user_id + "/musics",
                                                success: (json) => {
                                                    // console.log(json)
                                                    for (let i = 0; i < json.length; i++){
                                                        $('.music-list').append('<li data-id=' + json[i].id +  '><input type="radio" name="music" value=' + json[i].id + '><a href=' + json[i].link + ' target="_blank">'
                                                        + json[i].name + '</a></li>')
                                                    }
                                                    $.ajax({
                                                        type: 'GET',
                                                        url: MyServer + user_id + "/friends",
                                                        success: (json) => {
                                                            // console.log(json)
                                                            for (let i = 0; i < json.length; i++){
                                                                let friend_id = json[i].friend_id;
                                                                for (let j = 0; j < users.length; j++){
                                                                    if (friend_id === users[j].id){
                                                                        $('.friend-list').append('<li data-id=' + users[j].id + '><a>'
                                                                        + users[j].first_name + '</a></li>')
                                                                    }
                                                                }                                                                
                                                            }
                                                            $.ajax({
                                                                type: 'GET',
                                                                url: MyServer + user_id + "/hobbies",
                                                                success: (json) => {
                                                                    // console.log(json)
                                                                    for (let i = 0; i < json.length; i++){
                                                                        $('.hobby-list').append('<li data-id=' + json[i].id +  '><input type="radio" name="hobby" value=' + json[i].id + '><a href=' + json[i].link + ' target="_blank">'
                                                                        + json[i].name + '</a></li>')
                                                                    }
                                                                }
                                                            })
                                                        }
                                                    })
                                                }
                                            })
                                        }
                                    })
                                }
                            })
                        }
                    })

                }
            })
        }

    })
})