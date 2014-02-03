var candidate_id;

$( "#candidate-search" ).autocomplete({
	 source: function( request, response ) {
		 
		 $.ajax({
			 url: $.config.search_url,
			 type: "GET",
			 data:{
				 item: request.term,
			 },
			 context: this,
			 success: function(json) {
	                json = JSON.parse(json);
	                
	                response($.map(json, function(item) {
	                	
	                	return {
	                		label: item.name,
	                		url: item.url,
	                		value: null,
	                	}
	                }));
			 },
		 });
		 return response
	 },
	 select: function( event, ui ) {
		 window.location = ui.item.url;
	 }

});
