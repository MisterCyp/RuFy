$(document).ready( function() {

    $("#btn-search").click( function(event) {
        recherche();
    });
});

$('div button').click(function() {
	
    $btn = $(this);
	var cat = $btn.attr("name");
    cat = "#tab-"+cat;
    $(cat).inertAfter("#btns-categories");
	
});

function recherche() {
    if ($("#champs").val())
            location.href = Urls['t411:search']($("#champs").val());
}

$(function () {

        // Settings
        var $widget = $("#btns-categories");
            $('#btns-categories').find('button').each(
            function() { // This doesn't work because the .div_item children aren't populated?
                    $(this).on('click',function(){
                    var cat = $(this).attr('name');
                    cat = "#tab-"+cat;  
                    $(cat).insertAfter("#btns-categories");  
                        });
                    
                });
                
            
    });
    
$(function () {       
        $('#btn-download').click(function() {
            var arguments = $(this).attr("value").split("-");
                    $.ajax({
          url      : Urls['t411:download'](arguments[0],arguments[1]), 
          cache    : false,
          dataType : "text",
          success : function(reponse, statut){
												
															 if($.trim(reponse)=='success')
															 {
																 
																$(".alert-success").show("slow");
																setTimeout(function(){
																	  $(".alert-success").hide("slow");
																	}, 4000); 
															 }
															 if($.trim(reponse)=='dossier')
															 {
																$(".alert-danger").show("slow");
																setTimeout(function(){
																	  $(".alert-danger").hide("slow");
																	}, 4000); 
															 }
															
    
 
														},
          error : function(resultat, statut, erreur){
							console.log(resultat);
							console.log(statut);
							console.log(erreur);
                                                        alert("La SeedBox ne repond pas !")

														},
          complete : function(resultat, statut){

														}   
     });     
                        });
});

$(function () { 
    $('.table').each(function () {
    $(this).DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.11/i18n/French.json"
        },
        "order": [[ 3, "desc" ]]
    });
    });
});

$(function () { 
$('#'+$('#select_cat').val()).show();
    
$( "#select_cat" ).change(function() {
  $('.sub-cat').each(function () {
    $(this).hide()
    });
    
  $('#'+$(this).val()).show();
});

});
