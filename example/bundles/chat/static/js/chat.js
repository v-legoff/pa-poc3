/**
 * This file contains the chat mechanism, suing jQuery, a websocket connection
 * and more.
 */

$(document).ready(function() {
    
    // Variable definitions
    var sounds = new Array();
    
    // When the page is loaded
    $('#connected_list').hide();
    
    // Websocket connection
    var ws = $.websocket("ws://localhost:9000/ws", {
        events: {
            error: function(e) {
                message = e.data.message;
                $('#history').html($('#history').html() + "<br />" + $('#last_message').html());
                $('#last_message').html("<strong>" + message + "</strong>");
            },
            message: function(e) {
                message = e.data.message;
                $('#history').html($('#history').html() + "<br />" + $('#last_message').html());
                $('#last_message').html(message);
                $('#snd_message')[0].play();
            },
            setpseudo: function(e) {
                pseudo = e.data.pseudo;
                newpseudo = e.data.newpseudo;
                if(newpseudo)
                {
                    $('#instruction').text('Your current pseudo');
                    $('#setpseudo').val('Change');
                    $('#snd_connect')[0].play();
                }
            },
            update_online: function(e) {
                nb_online = e.data.nb_online;
                pseudos = e.data.pseudos;
                if (nb_online == 0) 
                {
                    message = "There is nobody connected yet";
                    $('#connected_list').html("");
                }
                else if (nb_online == 1)
                {
                    message = "There is one people online";
                    $('#connected_list').html('<ul><li>' + pseudos[0] + '</li></ul>');
                }
                else
                {
                    message = "There are " + nb_online + " people online";
                    code = "<ul>";
                    for (i = 0; i < pseudos.length; i++)
                    {
                        code += '<li>' + pseudos[i] + '</li>';
                    }
                    code += '</ul>';
                    $('#connected_list').html(code);
                }
                $('#nb_online').text(message);
            }
        }
    });
    
    $('#detail_connected').click(function() {
        if($('#connected_list').is(':visible'))
        {
            $('#connected_list').hide();
            $(this).text('show the list');
        }
        else
        {
            $('#connected_list').show();
            $(this).text('hide the list');
        }
        return false;
    });
    
    $('#setpseudo').click(function() {
        pseudo = $('#pseudo').val();
        ws.send("setpseudo", {"pseudo": pseudo});
        return false;
    });

    $('#send').click(function() {
        ws.send("message", {"message": $('#message').val()});
        $('#message').val("");
        return false;
    });
    
    $('#audio_test').click(function() {
        var basefile = $('#sound_test option:selected').attr('id');
        var oggFile = "/static/sounds/" + basefile + ".ogg";
        var mp3File = "/static/sounds/" + basefile + ".mp3";
        var audio = $('#snd_test')[0];
        $('#ogg_test').attr('src', oggFile);
        $('#mp3_test').attr('src', mp3File);
        audio.load();
        audio.play();
        return false;
    });

    $('#sound_settings').click(function() {
        code = "<h2>Sounds settings</h2>";
        code += "<ul>";
        for (i = 0; i < sounds.length; i++)
        {
            code += '<li>' + sounds[i] + '</li>';
        }
        code += '</ul>';
        $('#settings_tab').html(code);
        return false;
    });
});