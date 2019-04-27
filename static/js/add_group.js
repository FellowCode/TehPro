$(document).ready(function () {
   $('#add_worker').click(function () {
       $('#worker-select').clone().appendTo('#worker-list')
   });
});