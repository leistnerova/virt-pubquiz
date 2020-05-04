function run_countdown() {
    $('#btn-countdown').prop('disabled', true);
    $.ajax({
        url: '/api/run/countdown',
        success: function (data) {
            if (data) {
                $('#btn-countdown').text(data['countdown']);
                if (data['countdown'] <= 6) {
                    update_countdown(1000);
                }
                if (!data['countdown']) {
                    stop_countdown();
                }
            }
            else {
                stop_countdown();
            }
        }
    })
}

function start_countdown(interval) {
    window.countdown = setInterval(run_countdown, interval);
}

function stop_countdown() {
    clearInterval(window.countdown)
    $('#btn-update').prop('disabled', true);;
    $('#answer').prop('disabled', true);;
}

function update_countdown(interval) {
    clearInterval(window.countdown)
    window.countdown = setInterval(run_countdown, interval);
}
