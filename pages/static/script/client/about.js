#!/usr/bin/node

$(document).ready(function () {
    let desc = $('.description').html()
    let button = $('.crud').html()
    let server = 'http://52.201.220.122/api/v1/'
    let fullname, contact;
            $.ajax({
                type: 'GET',
                url: 'http://web-02.besufikadyilma.tech/session',
                success: (json) => {
                    $.ajax({
                        type: 'GET',
                        url: server + 'users',
                        success: (json2) => {
                            for (let i = 0; i < json2.length; i++) {
                                if (json.email === json2[i].email) {
                                    user_id = json2[i].id;
                                    if (json2[i].first_name != undefined && json2[i].last_name != undefined) {
                                        $('.desc-name').append(json2[i].first_name + " " + json2[i].last_name)
                                    } else if (json2[i].first_name !=undefined) {
                                        $('.desc-name').append(json2[i].first_name)
                                    }
                                    if (json2[i].contact != undefined) {
                                        $('.desc-contact').append(json2[i].contact)
                                    }
                                }
                            }                
                    }
                })
            }
        
        })

    $('.edit').click(function () {
        $('.crud').text("")
        $('.crud').append('<button class="save">' + 
                          'Save' + 
                          '</button>' + 
                          '<button class="cancel">' + 
                          'Cancel' + 
                          '</button>'
                          );
        $('.description').text("")
        let form = '<form>' + 
                   '<input type="text" class="f-name" name="fName" placeholder="First Name*">' +
                   '<input type="text" class="l-name" name="lName" placeholder="Last Name*">' +
                   '<input type="text" class="contact" name="Name*" placeholder="Contact">' +
                   '</form>';
        $('.description').append(form);

        $('.cancel').click(() => {
            if (confirm('Are u sure u want  to cancel?')){
                $('.crud').text("")
                $('.description').text("")
                $('.crud').html(button)
                $('.description').html(desc)
                location.reload(true)
            }

        })

        $('.save').click(() => {
            let user_id;
            $.ajax({
                type: 'GET',
                url: 'http://web-02.besufikadyilma.tech/session',
                success: (json) => {
                    $.ajax({
                        type: 'GET',
                        url: server + 'users',
                        success: (json2) => {
                            for (let i = 0; i < json2.length; i++) {
                                if (json.email === json2[i].email) {
                                    user_id = json2[i].id;
                                }
                            }
                            $.ajax({
                                type: 'PUT',
                                url: server + user_id + '/user',
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'first_name': $('input.f-name').val(),
                                    'last_name': $('input.l-name').val(),
                                    'contact': $('input.contact').val(),
                                }),
                                success: (json3) => {
                                    location.reload(true)
                                    console.log($('.input.f-name').val())
                                }
                            })                 
                        }
                    })
                }
            
            })
        })
    })
    $('.delete').click(() => {
       if (confirm("Are U sure u want to delete ur account?")){
        let user_id;
        $.ajax({
            type: 'GET',
            url: 'http://web-02.besufikadyilma.tech/session',
            success: (json) => {
                $.ajax({
                    type: 'GET',
                    url: server + 'users',
                    success: (json2) => {
                        for (let i = 0; i < json2.length; i++) {
                            if (json.email === json2[i].email) {
                                user_id = json2[i].id;
                              }
                           }
                           $.ajax({
                               type: 'DELETE',
                               url: server + user_id + '/' + 'delete_account',
                               success: (json3) => {
                                    location.replace('/logout')
                            }
                    })                 
                }
            })
        }
     
    })
       }
    })
})