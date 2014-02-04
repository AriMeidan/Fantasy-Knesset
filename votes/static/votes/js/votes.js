// takes 0 or 1 and returns the opposite
$.numToggle = function(input) {
    if (input == 1) {return 0;}
    return 1;
}

$( document ).ready(function() {

    // apply classes and text according to value
    $( ".btn-candidate" ).each(function() {
        var value = $( this ).attr("upvote");
        $( this ).addClass($.config.btn_class[value]);
        $( this ).text($.config.vote_text[value])
    });

    // buttons on click AJAX
    $( ".btn-candidate" ).click(function( event ) {

        $.ajax({
            url: $.config.vote_url,
            type: "POST",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
            },
            data: {
                upvote: $( this ).attr("upvote"),
                candidate_pk: $( this ).attr("pk"),
            },
            context: this,  // set this as the context of any callback function
            success: function(json) {
                json = JSON.parse(json);
                if (json.success == true) {
                    var oldButtonValue = $( this ).attr("upvote");
                    $( this ).removeClass($.config.btn_class[oldButtonValue]);
                    var newButtonValue = $.numToggle(oldButtonValue);
                    $( this ).attr("upvote", newButtonValue);
                    $( this ).addClass($.config.btn_class[newButtonValue]);
                    $( this ).text($.config.vote_text[newButtonValue]);
                } else {
                    console.log("error: ajax call succeeded but without success value = true");
                }
            },
            error: function( xhr, status ) {
                window.location.replace($.config.login_url);
            },
        });
    });
});