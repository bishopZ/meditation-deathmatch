
var track_mellow = [0.0, 0.0];
var track_score = [0.0, 0.0];
var timer_tracking;
var clock;
var two_player_mode = true;
var game_started = false;
var fft_widgets = [{}, {}];
var socket;


function chart_update_for_data(player, channel, data) {
    var clip = 0;
    data[0] = clip;
    fft_widgets[player].channelData[channel] = data;
}


function handle_packet(packet) {
    headset = packet['headset'] - 1;
    path = packet['path'];
    args = packet['args'];
    if (path == '/muse/elements/experimental/mellow') {
        var height = Math.floor(400 * args[0]);
        track_mellow[headset] = args[0];
        if (headset == 0) {
            $('#mellow0').height(height);
        }
        if (headset == 1) {
            $('#mellow1').height(height);
        }
    } 
    else if (path == '/muse/elements/raw_fft0' || path == '/muse/elements/raw_fft1' || path == '/muse/elements/raw_fft2' || path == '/muse/elements/raw_fft3') {
        if (headset == 0) {
            if (path == '/muse/elements/raw_fft0') {
                chart_update_for_data(0, 0, args);
            }
            if (path == '/muse/elements/raw_fft1') {
                chart_update_for_data(0, 1, args);
            }
            if (path == '/muse/elements/raw_fft2') {
                chart_update_for_data(0, 2, args);
            }
            if (path == '/muse/elements/raw_fft3') {
                chart_update_for_data(0, 3, args);
            }
        }
        if (headset == 1 && two_player_mode) {
            if (path == '/muse/elements/raw_fft0') {
                chart_update_for_data(1, 0, args);
            }
            if (path == '/muse/elements/raw_fft1') {
                chart_update_for_data(1, 1, args);
            }
            if (path == '/muse/elements/raw_fft2') {
                chart_update_for_data(1, 2, args);
            }
            if (path == '/muse/elements/raw_fft3') {
                chart_update_for_data(1, 3, args);
            }
        }
    }
    else {
        //console.log(JSON.stringify(packet, null, 4));
    }
}


function pad(val, pad) {
    str = '';
    for (i = 0; i < pad; i++) {
        str = String(str + '0');
    }
    return String(str+val).slice(-1 * pad);
}


function player_text(score, clock, minutes, seconds) {
    var clock_txt = minutes + ':' + pad(seconds, 2);
    if (clock == 0) {
        clock_txt = 'Final';
    }
    return 'Score: ' + pad(score, 4) + ' - ' + clock_txt;
}


function update_game_display() {
    var minutes = Math.floor(clock / 60);
    var seconds = clock - minutes * 60;
    $('#head0').html(player_text(track_score[0], clock, minutes, seconds));
    $('#head1').html(player_text(track_score[1], clock, minutes, seconds));
}


function start_game() {
    if (!game_started) {
        game_started = true;
        track_score = [0.0, 0.0];
        clock = 180;
        update_game_display();
        timer_tracking = setInterval(function() {
            clock = clock - 1;
            if (clock <= 0) {
                window.clearInterval(timer_tracking);
            }
            for (i = 0; i < 2; i++) {
                scaled = track_mellow[i] * 100;
                if (scaled > 90) {
                    track_score[i] += 15;
                } else if (scaled > 80) {
                    track_score[i] += 3;
                } else if (scaled > 75) {
                    track_score[i] += 1;
                }
            }
            update_game_display();
        }, 1000);
    }
}


function show_fft(container) {
    var container_height = 400;
    var container_width = 500;
    var fftwidget = new FFTWidget(container_width, container_height);
    fftwidget.renderer.backgroundColor = 0xFFFFFF;
    fftwidget.demoMode = false;
    fftwidget.maxFrequencyBin = 128;
    container.html(fftwidget.getView());
    fftwidget.animate();
    return fftwidget;
}


$(document).ready(function() {
    fft_widgets[0] = show_fft($('#displayPlayer1').first());
    fft_widgets[1] = show_fft($('#displayPlayer2').first());

    socket = io.connect();
    socket.emit('request_init_lights');
    socket.on('packet', function(packet) {
        handle_packet(packet);
    });
    $("#connect0").bind("click", function(event) {
        console.log("stuff ...");
        socket.emit('request_connect_one');
    });
    $("#connect1").bind("click", function(event) {
        console.log("stuff ...");
        socket.emit('request_connect_two');
    });
    $("#disconnect0").bind("click", function(event) {
        socket.emit('request_disconnect_one');
    });
    $("#disconnect1").bind("click", function(event) {
        socket.emit('request_disconnect_two');
    });
    $("#listheadsets").bind("click", function(event) {
        console.log("stub");
    });
    $("#start").bind("click", function(event) {
        start_game();
    });
    $("#reset").bind("click", function(event) {
        $('#head0').html('Player 1');
        $('#head1').html('Player 2');
    });
    $("#lights").bind("click", function(event) {
        socket.emit('request_init_lights');
    });
});

