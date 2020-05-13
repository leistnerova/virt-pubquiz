$(document).ready(function(){

    $('#question-id').val('')
    if ($('#btn-update').length) window.is_editor = true;
    else window.is_editor = false;

    if (window.is_editor) {
        $('#btn-update').click(function(event) {
            event.preventDefault();
            $.ajax({
                url: '/api/play/answer/' + $('#team-id').val() + '/' + $('#question-id').val(),
                data: {'text': $('#answer').val()},
                type: 'POST',
                success: function (data) {
                    $('#answer-msg').html('<div class="alert alert-success">Answer was updated.</div>');
                }
            });
        });
    }

    setInterval(function() {

        $('#answer-msg').html('')

        // load actual question/category
        $.ajax({
            url: '/api/play/actual',
            success: function (data) {
                if (data['question_id'] != $('#question-id').val()) {
                    $('#actual-item').html(data['html']);
                    $('#question-id').val(data['question_id']);
                    if (data['answer']) {
                        $('#answer-div').show();
                        $('#answer-div').html(data['answer']);
                    }
                    else {
                        if (window.is_editor) {
                            $('#btn-update').prop('disabled', false);
                            $('#answer').prop('disabled', false);
                        }
                        $('#answer').val('');
                        stop_countdown()
                        $('#btn-countdown').hide();
                        if (!data['question_id'] || data['question_id'] < 0) {
                            $('#answer-div').hide();
                        }
                        else {
                            if (window.is_editor) {
                                $('#btn-update').prop('disabled', true);
                                $('#answer').prop('disabled', true);
                            }
                            $('#answer-div').show();
                        }
                    }
                }
            }
        });

        // check if countdown started
        if (!$('#btn-countdown').is(':visible')) {
            $.ajax({
                url: '/api/run/countdown',
                success: function (data) {
                    if (data) {
                        if (window.is_editor) {
                            $('#btn-update').prop('disabled', false);
                            $('#answer').prop('disabled', false);
                        }
                        $('#btn-countdown').show();
                        $('#btn-countdown').text(data['countdown']);
                        start_countdown(5000)
                    }
                }
            });
        }

        // load answer
        if (!window.is_editor && $('#question-id').val() > 0) {
            $.ajax({
                url: '/api/play/answer/' + $('#team-id').val() + '/' + $('#question-id').val(),
                success: function (data) {
                    $('#answer').val(data);
                }
            });
        }

        // load members
        $.ajax({
            url: '/api/teams/' + $('#team-id').val() + '/members',
            success: function (data) {
                $('#members').text(data);
            }
        });
    }, 1000);
});

