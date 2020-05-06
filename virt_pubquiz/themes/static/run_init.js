$(document).ready(function(){
    $('#btn-category').click(function() {
        $.ajax({
            url: '/api/run/showcategory',
            data: {'type': 'actual'},
            type: 'POST',
            success: function (data) {
                $('#btn-category').prop('disabled', true);
                $('#btn-activate').prop('disabled', false);
            }
        });
    });
});
