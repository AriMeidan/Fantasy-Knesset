function searchListener() {

	var search = document.getElementById("candidate-search").value;	

	var accordion = document.getElementById("accordion")

	var coll = accordion.getElementsByClassName("collapse")
	var cand = accordion.getElementsByClassName("panel-body")

	// if the search term is not empty open every collapsible and hide non-searched
	if (search != ""){

		// open every collapsible
		// first "out" and then "in" for every collapsible
		for(var i = 0; i < coll.length; i++){ coll[i].classList.remove("out"); }
		for(var i = 0; i < coll.length; i++){ coll[i].classList.add("in"); }

		// hide non-searched
		for(var i = 0; i < cand.length; i++){
			id = cand[i].id;
			if(id.indexOf(search) == -1){
				cand[i].hidden = true;
			} else {
				cand[i].hidden = false;
			}
		}


	// else, collapse and show all hidden
	} else {
		for(var i = 0; i < coll.length; i++){ coll[i].classList.remove("in"); }			
		for(var i = 0; i < coll.length; i++){ coll[i].classList.add("out"); }

		for(var i = 0; i < cand.length; i++){
			cand[i].hidden = false;
		}
	}
}

// add event listener to t
var searchElement = document.getElementById("candidate-search");
searchElement.addEventListener("change", searchListener, false);