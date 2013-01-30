/**
 * This file contains the chat mechanism, suing jQuery, a websocket connection
 * and more.
 */

$(document).ready(function() {
    
    // When the page is loaded
    $('#connected_list').hide();
    $('#settings').hide();
    $('div.settings_tab').hide();
    $('#settings_sounds').show();
    
    // Websocket connection
    var ws = $.websocket("ws://localhost:9000/ws", {
        events: {
            error: function(e) {
                var message = e.data.message;
                var last_message = $('#last_message').html();
                var history = $('#history').html();
                $('#history').html(history + "<br />" + last_message);
                $('#last_message').html("<strong>" + message + "</strong>");
            },
            message: function(e) {
                var message = e.data.message;
                var message = e.data.message;
                var last_message = $('#last_message').html();
                var history = $('#history').html();
                $('#history').html(history + "<br />" + last_message);
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
                if(nb_online == 0) 
                {
                    var message = "There is nobody connected yet";
                    $('#connected_list').html("");
                }
                else if(nb_online == 1)
                {
                    var message = "There is one people online";
                    var code = "<ul><li>" + pseudos[0] + "</li></ul>";
                    $('#connected_list').html(code);
                }
                else
                {
                    var message = "There are " + nb_online + " people online";
                    code = "<ul>";
                    for(i = 0; i < pseudos.length; i++)
                    {
                        code += "<li>" + pseudos[i] + "</li>";
                    }
                    code += "</ul>";
                    $('#connected_list').html(code);
                }
                $('#nb_online').text(message);
            }
        }
    });
    
    // Page events
    
    /**
     * When the link to show / hide the list of connected is clicked on
     */
    $('#detail_connected').click(function() {
        if($('#connected_list').is(':visible'))
        {
            $('#connected_list').hide();
            $(this).text("show the list");
        }
        else
        {
            $('#connected_list').show();
            $(this).text("hide the list");
        }
        return false;
    });
    
    /**
     * When the pseudo is set or change
     */
    $('#setpseudo').click(function() {
        var pseudo = $('#pseudo').val();
        ws.send("setpseudo", {"pseudo": pseudo});
        return false;
    });
    
    /**
     * When the send button is clicked on
     */
    $('#send').click(function() {
        var message = $('#message').val();
        ws.send("message", {"message": message});
        $('#message').val("");
        return false;
    });
    
    /**
     * Display or hide the settings tab
     * If the setting tab is visible, the configuration set is not applied
     * To apply the configuration set, the user must press the 'save' button
     */
    $('#toggle_settings').click(function() {
        if($('#settings').is(':visible'))
        {
            $('#settings').hide();
        }
        else
        {
            $('#settings').show();
        }
        return false;
    });
    
    /**
     * Test the selected audio file
     */
    $('button.btn_test').click(function() {
        var btn_id = $(this).attr('id');
        var gen_id = btn_id.substring(4);
        var select_id = "sel_" + gen_id;
        var sel = '#' + select_id + ' option:selected';
        var basefile = $(sel).attr("value");
        var oggFile = "/static/sounds/" + basefile + ".ogg";
        var mp3File = "/static/sounds/" + basefile + ".mp3";
        var audio = $('#snd_test')[0];
        $('#ogg_test').attr('src', oggFile);
        $('#mp3_test').attr('src', mp3File);
        audio.load();
        audio.play();
        return false;
    });
    
    function save_sounds_settings()
    {
        $('#settings_sounds select').each(function(index) {
            var select_id = $(this).attr('id');
            var event_id = select_id.substring(4);
            var choice = $(this).children('option:selected').attr('value');
            var oggFile = "/static/sounds/" + choice + ".ogg";
            var mp3File = "/static/sounds/" + choice + ".mp3";
            var audio = $('#snd_' + event_id)[0];
            $('#snd_' + event_id + '_ogg').attr('src', oggFile);
            $('#snd_' + event_id + '_mp3').attr('src', mp3File);
            audio.load();
        });
    }
    
    function save_settings()
    {
        // Try to find the visible div
        var current_id = $('div.settings_tab:visible').attr('id');
        var parameter = current_id.substring(9);
        if(parameter == "sounds")
        {
            save_sounds_settings();
        }
    }
    
    $('a.tab_setting').click(function() {
        // Get the name of the pressed link
        var name = $(this).text();
        name = name.toLowerCase();
        var tab_id = '#settings_' + name;
        save_settings();
        $('div.settings_tab').hide();
        $(tab_id).show();
        return false;   
    });
    
    $('#save_settings').click(function() {
        save_settings();
        $('#settings').hide();
        return false;
    });
    
    $('#close_settings').click(function() {
        $('#settings').hide();
        return false;
    });
});