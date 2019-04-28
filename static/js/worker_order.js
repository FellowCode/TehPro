$(document).ready(function () {
    $('.datepicker').datepicker({
        selectMonths: true,
        selectYears: 3,
        format: 'dd.mm.yyyy'
    });

    $('.timepicker').timepicker({
        twelveHour: false
    });

    $('#add_work').click(function () {
        $('#work-select').clone().appendTo('#work-list')
    });

    $('.counter-input a.counter').each(function (index) {
        $(this).click(function () {
            var target = $(this).data('target');
            var type = $(this).attr('id');
            var step = $(this).data('step');
            if (typeof step === 'undefined')
                step = 1;
            else
                step = parseInt(step);
            var $input = $('input[name=' + target + ']');
            var val = parseInt($input.val());
            if (type === 'inc')
                val += step;
            if (type === 'dec' && val >= step)
                val -= step;
            $input.val(val)
        });
    });
});