// takes 0 or 1 and returns the opposite
$.numToggle = function(input) {
    if (input == 1) {return 0;}
    return 1;
}

$( document ).ready(function() {

    // apply classes and text according to value
    $( ".btn-candidate" ).each(function() {
        var value = $( this ).attr("value");
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
                upvote: $( this ).attr("value"),
                candidate_pk: $( this ).attr("name"),
            },
            context: this,  // set this as the context of any callback function
            success: function(json) {

                var oldButtonValue = $( this ).attr("value");
                $( this ).removeClass($.config.btn_class[oldButtonValue]);
                var newButtonValue = $.numToggle(oldButtonValue);
                $( this ).attr("value", newButtonValue);
                $( this ).addClass($.config.btn_class[newButtonValue]);
                $( this ).text($.config.vote_text[this.value]);
            },
        });

    });
});
