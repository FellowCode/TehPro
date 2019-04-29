$(document).ready(function () {
   $('#add_worker').click(function () {
       var $new_select = $('#worker-select').clone();
       $new_select.find('#delete-worker').click(function () {
           $(this).closest('#worker-select').remove();
       });
       $new_select.css('display', 'block');
       $new_select.appendTo('#worker-list')
   });
   $('#worker-select #delete-worker').each(function (index) {
       $(this).click(function () {
           console.log('aaa');
           $(this).closest('#worker-select').remove()
       });
   });
});