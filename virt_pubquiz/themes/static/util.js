function run_countdown() {
    $('#btn-countdown').prop('disabled', true);
    $.ajax({
        url: 'api/run/countdown',
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
    $('#answer').prop('disabled', true);;
    save_answer();
}

function update_countdown(interval) {
    clearInterval(window.countdown)
    window.countdown = setInterval(run_countdown, interval);
}

function save_points(team_id, question_id, points) {
    $('#message').html('');
    $.ajax({
        url: 'api/teams/' + team_id + '/answers/' + question_id + '/points',
        data: {'points': points},
        type: 'POST',
        success: function (data) {
            if (data['result'] != 'OK') {
                $('#message').html(data['error']);
            }
            else {
                $.ajax({
                    url: 'api/teams/' + team_id + '/points',
                    success: function (data) {
                        $('#team_' + team_id + '_points').html(data);
                    }
                })
            }
        }
    })
}

function save_answer() {
    answer_value = $('#answer').val()
    if (answer_value) {
        $.ajax({
            url: 'api/play/answer/' + $('#team-id').val() + '/' + $('#question-id').val(),
            data: {'text': answer_value},
            type: 'POST',
            success: function (data) {
                $('#answer-msg').html('Answer was updated.');
            }
        });
    }
}

function load_answer() {
    $.ajax({
        url: 'api/play/answer/' + $('#team-id').val() + '/' + $('#question-id').val(),
        success: function (data) {
            $('#answer').val(data);
        }
    });
}
