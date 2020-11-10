$(document).ready(function(){

    $('#question-id').val('')
    $.ajax({
        url: 'api/play/user',
        success: function (data) {
            if (data && data['editor'] == '1') {
                window.is_editor = true
            }
        }
    });

    $('#answer').keyup(save_answer);

    setInterval(function() {

        $('#answer-msg').html('')

        // load actual question/category
        $.ajax({
            url: 'api/play/actual',
            success: function (data) {
                if (data['question_id'] != $('#question-id').val()) {
                    $('#actual-item').html(data['html']);
                    $('#question-id').val(data['question_id']);
                    answer_div = $('#answer-div')
                    if (data['answer']) {
                        answer_div.show();
                        answer_div.html(data['answer']);
                    }
                    else {
                        answer = $('#answer')
                        if (window.is_editor && answer.prop('disabled')) {
                            $('#answer').prop('disabled', false);
                        }
                        answer.val('');
                        answer.prop('placeholder', '');
                        stop_countdown()
                        $('#btn-countdown').hide();
                        if (!data['question_id'] || data['question_id'] < 0) {
                            answer_div.hide();
                        }
                        else {
                            if (window.is_editor) {
                                answer.prop('disabled', true);
                            }
                            answer_div.show();
                        }
                    }
                }
            }
        });

        // check if countdown started
        btn_countdown = $('#btn-countdown');
        if (!btn_countdown.is(':visible')) {
            $.ajax({
                url: 'api/run/countdown',
                success: function (data) {
                    if (data) {
                        if (window.is_editor && data['countdown'] != 0) {
                            answer = $('#answer');
                            load_answer();
                            if (answer.prop('disabled')) {
                                answer.prop('disabled', false);
                                answer.prop('placeholder', 'Type your answer');
                                answer.focus()
                            }
                        }
                        $('#btn-countdown').show();
                        $('#btn-countdown').text(data['countdown']);
                        if (data['countdown'] != 0) start_countdown(5000)
                    }
                }
            });
        }
        else {
            if (!(window.is_editor && btn_countdown.text() && btn_countdown.text() != '0')) {
                load_answer();
            }
        }

        // load answer
        if (!window.is_editor && $('#question-id').val() > 0) {
            load_answer();
        }

        // load members
        $.ajax({
            url: 'api/teams/' + $('#team-id').val() + '/members',
            success: function (data) {
                $('#members').text(data);
            }
        });
    }, 1000);
});

