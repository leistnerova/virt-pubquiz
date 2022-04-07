$(document).ready(function(){
    $('#btn-category').click(function() {
        $.ajax({
            url: 'api/run/showcategory',
            data: {'type': 'next'},
            type: 'POST',
            success: function (data) {
                $('#btn-category').prop('disabled', true);
                $('#btn-next').prop('disabled', false);
                $('#btn-countdown').hide();
                $('#answer').hide();

                $.ajax({
                    url: 'api/run/category',
                    success: function (data) {
                        $('#actual-item').html(data['html']);
                    }
                });
            }
        });
    });

    $('#btn-next').click(function() {
        $.ajax({
            url: 'api/run',
            data: {'next': '1'},
            type: 'POST',
            success: function (data) {
                if (data['result'] == 'OK') {
                    $.ajax({
                        url: 'api/run/actual',
                        success: function (data) {
                            $('#actual-item').html(data['html']);
                            if (data['answer']) {
                                $('#answer').html(data['answer']);
                                $('#answer').show();
                            }
                        }
                    });
                    $.ajax({
                        url: 'api/run/next',
                        success: function (data) {
                            $('#next-item').html(data['html']);
                            if (!data['question_id']) {
                                $('#btn-next').hide();
                                $('#btn-reload').show();
                                $('#next-item').hide();
                            }
                        }
                    });
                    $.ajax({
                        url: 'api/run/category',
                        success: function (data) {
                            if (data['next_category_id'] && data['actual_category_id'] != data['next_category_id']) {
                                $('#btn-category').prop('disabled', false);
                                $('#btn-category').show();
                                $('#btn-next').prop('disabled', true);
                            }
                            else {
                                $('#btn-category').hide();
                            }
                        }
                    });
                    stop_countdown();
                    $('#btn-countdown').show();
                    $('#btn-countdown').text('Start countdown');
                    $('#btn-countdown').prop('disabled', false);
                }
            }
        });
    });

    $('#btn-countdown').click(function() {
        $.ajax({
            url: 'api/run/start',
            success: function (data) {
                $.ajax({
                    url: 'api/run/countdown',
                    success: function (data) {
                        $('#btn-countdown').text(data['countdown']);
                    }
                });
                start_countdown(5000);
            }
        });
    });

    $('#btn-thanks').click(function() {
        $.ajax({
            url: 'api/run/showthanks',
            type: 'GET',
            success: function (data) {
                $('#btn-thanks').prop('disabled', true);
            }
        });
    });
});
