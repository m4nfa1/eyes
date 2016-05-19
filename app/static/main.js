// ----- custom js ----- //

$('#path').click(function(){
    $("#file").click();
});

$('#file').on('change', function() {
	var file = $('#file')[0].files[0]['name'];
	$('#path').val(file);
});

$('#upload').click(function(){
 	$("#loader").show();
});