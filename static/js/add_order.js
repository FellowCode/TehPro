$(document).ready(function () {
    //$('.datepicker').datepicker();
    $('.datepicker').datepicker({
        selectMonths: true,
        selectYears: 3,
        format: 'dd.mm.yyyy'});

    $('.timepicker').timepicker({
        twelveHour: false});
});