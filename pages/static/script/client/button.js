#!/usr/bin/node

function listner (button, erase_list, erase_crud, type, name) {
    let user_id;
    let MyServer = "http://127.0.0.1:5001/api/v1/"
    $(button).click(() => {
        var $this = $(this);
    let list = $(erase_list).html();
    let crud = $(erase_crud).html()

        // console.log(list)
        if($this.data('clicked')) {
        } else {
            let form = '<form>' + 
            '<input type="text" class=' + type + '1 name="Name*" placeholder="name*">' +
            '<input type="text" class=' + type + '2 name="Link" placeholder="link">' +
             
            '<input type="text" class=' + type + '3 name="Description" placeholder="description">'
            if (type === 'book') {
            form += '<input type="text" class=' + type + '4 name="Name*" placeholder="author*">' 
            }
            form += '</form>'
            $(erase_list).text("");

            if (type != 'friend') {
            $(erase_list).append(form);
            }

            $(erase_crud).text("");
            $(erase_crud).append('<button class=' + type + '-save' + '>Save</button>');
            $(erase_crud).append('<button class=' + type + '-cancel' + '>Cancel</button>');


            $('.' + type + '-cancel').on('click', () =>{
                            if(confirm('Are u sure u want to cancel?')){
                            $(erase_list).text("");
                            $(erase_crud).text("");
                            $(erase_list).html(list);
                            $(erase_crud).html(crud);
                        }
                    })
            $('.' + type + '-save').on('click', () => {
                // console.log($('input.port').val())
                $.ajax({
                    type: 'GET',
                    url: 'http://127.0.0.1:5002/session',
                    success: (json) => {
                        $.ajax({
                            type: 'GET',
                            url: MyServer + 'users',
                            success: (json2) => {
                                for (let i = 0; i < json2.length; i++) {
                                    if (json.userinfo.email === json2[i].email) {
                                        user_id = json2[i].id;
                                    }
                                }
                                let port_name = 'input.' + type + '1';
                                console.log($(port_name).val())
                                let link = 'input.' + type + '2';
                                let description = 'input.' + type + '3';
                                $.ajax({
                                    type: 'POST',
                                    url: MyServer + user_id + '/' + name,
                                    contentType: 'application/json',
                                    data: JSON.stringify({
                                        'name': $(port_name).val(),
                                        'link': $(link).val(), 
                                        'description': $(description).val(),
                                        'author': $('input.' + type + '4').val()
                                    }),
                                    success : (json) => {
                                        $(erase_list).text("");
                                        $(erase_crud).text("");
                                        $(erase_list).html(list);
                                        $(erase_crud).html(crud);  
                                    }
                                })
                            }
                        })
                    }

                })                  
            })
            }
        })    
}

function delete_item (id, name) {
    if (confirm("Are u sure want to delete?")){
    let user_id;
    let MyServer = "http://127.0.0.1:5001/api/v1/"
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5002/session',
        success: (json) => {
            $.ajax({
                type: 'GET',
                url: MyServer + 'users',
                success: (json2) => {
                    for (let i = 0; i < json2.length; i++) {
                        if (json.userinfo.email === json2[i].email) {
                            user_id = json2[i].id;
                        }
                    }
                    $.ajax({
                        type: 'DELETE',
                        url: MyServer + user_id + '/' + name + '/' + id,
                        success: (json) => {
                            location.reload(true)
                        }
                    })
                }
            })
        }
    })
  }
}

$(document).ready(function () {
   $('.port-add').click(listner('.port-add', '.port-list', '.port-crud', 'port', 'portfolios'))
   $('.book-add').click(listner('.book-add', '.book-list', '.book-crud', 'book', 'books'))    
   $('.movie-add').click(listner('.movie-add', '.movie-list', '.movie-crud', 'movie', 'movies'))
   $('.music-add').click(listner('.music-add', '.music-list', '.music-crud', 'music', 'musics'))
   $('.friend-add').click(listner('.friend-add', '.friend-list', '.friend-crud', 'friend', 'friends'))
   $('.hobby-add').click(listner('.hobby-add', '.hobby-list', '.hobby-crud', 'hobby', 'hobbies'))
   $('.port-delete').click(() => {
    delete_item($('.port-list input[type="radio"]:checked').val(), 'portfolios')
   })
   $('.book-delete').click(() => {
    delete_item($('.book-list input[type="radio"]:checked').val(), 'books')
   })
   $('.movie-delete').click(() => {
    delete_item($('.movie-list input[type="radio"]:checked').val(), 'movies')
   })
   $('.music-delete').click(() => {
    delete_item($('.music-list input[type="radio"]:checked').val(), 'musics')
   })
//    $('.friend-delete').click(() => {
//     delete_item($('.port-list input[type="radio"]:checked').val(), 'portfolios')
//    })
   $('.hobby-delete').click(() => {
    delete_item($('.hobby-list input[type="radio"]:checked').val(), 'hobbies')
   })
})