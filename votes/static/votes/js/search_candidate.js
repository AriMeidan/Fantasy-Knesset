/*
Copyright 2014 Ari Meidan and Tom Gurion

This file is part of "Games of Knesset".

"Games of Knesset" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Games of Knesset" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with "Games of Knesset".  If not, see <http://www.gnu.org/licenses/>.
*/

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
