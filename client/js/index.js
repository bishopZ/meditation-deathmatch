
var total_p1_packets = 0;
var packets_between_refresh = 4;
var fft_since_last_refresh = [packets_between_refresh, packets_between_refresh];
var track_mellow = [0.0, 0.0];
var track_score = [0.0, 0.0];
var timer_tracking;
var clock;
var start = new Date().getTime();
var end = new Date().getTime();
var two_player_mode = true;
var game_started = false;

var socket;

function chart_update_for_data(sel, data) {
    var clip = 1000;
    data[0] = clip;
    d3.select(sel).selectAll("div.bar")
        .data(data)
        .style("height", function(d) {
            var value = (d > clip) ? clip : d;
            var barHeight = Math.floor(value / 20.0);
            return barHeight + "px";
        });
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
            total_p1_packets += 1;
            if (total_p1_packets % 50 == 0) {
                end = new Date().getTime();
                var time = end - start;
                start = end;
                //console.log('Cycle time: ' + time);
            }
            if (fft_since_last_refresh[0] >= packets_between_refresh) {
                if (path == '/muse/elements/raw_fft0') {
                    chart_update_for_data("#myChart0", args);
                }
                if (path == '/muse/elements/raw_fft1') {
                    chart_update_for_data("#myChart1", args);
                }
                if (path == '/muse/elements/raw_fft2') {
                    chart_update_for_data("#myChart2", args);
                }
                if (path == '/muse/elements/raw_fft3') {
                    chart_update_for_data("#myChart3", args);
                }
                fft_since_last_refresh[0] = 0;
            }
            else {
                fft_since_last_refresh[0] += 1;
            }
        }
        if (headset == 1 && two_player_mode) {
            if (fft_since_last_refresh[1] >= packets_between_refresh) {
                if (path == '/muse/elements/raw_fft0') {
                    chart_update_for_data("#myChart4", args);
                }
                if (path == '/muse/elements/raw_fft1') {
                    chart_update_for_data("#myChart5", args);
                }
                if (path == '/muse/elements/raw_fft2') {
                    chart_update_for_data("#myChart6", args);
                }
                if (path == '/muse/elements/raw_fft3') {
                    chart_update_for_data("#myChart7", args);
                }
                fft_since_last_refresh[1] = 0;
            }
            else {
                fft_since_last_refresh[1] += 1;
            }
        }
    }
    else {
        //console.log(JSON.stringify(packet, null, 4));
    }
}


function setup_chart(sel, data) {
    d3.select(sel).selectAll("div.bar")
        .data(data)
        .enter()
        .append("div")
        .attr("class", "bar")
        .style("height", function(d) {
            var barHeight = d * 5;
            return barHeight + "px";
        });
}


function setup_initial_data() {
    dataset = [];
    for (i = 0; i < 120; i++) {
        dataset[i] = 15;
    }
    setup_chart("#myChart0", dataset);
    setup_chart("#myChart1", dataset);
    setup_chart("#myChart2", dataset);
    setup_chart("#myChart3", dataset);
    setup_chart("#myChart4", dataset);
    setup_chart("#myChart5", dataset);
    setup_chart("#myChart6", dataset);
    setup_chart("#myChart7", dataset);
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


$(document).ready(function() {
    setup_initial_data();
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

