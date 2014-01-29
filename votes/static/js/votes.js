// takes 0 or 1 and returns the opposite
$.numToggle = function(input) {
    if (input == 1) {return 0;}
    return 1;
}

$( document ).ready(function() {

    $( ".candidate-btn" ).click(function( event ) {

        $.ajax({
            url: $.config.vote_url,
            type: "POST",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
            },
            data: {
                upvote: this.value,
                candidate_pk: this.id,
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
