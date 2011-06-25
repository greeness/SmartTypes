
$(document).ready(
    function () {
        bind_side_nav_click_handler();
    }
);


var _href = ''
var bind_side_nav_click_handler = function(){
    $('#side_nav a').click(function(e){

        $('#side_nav a').removeClass('active');
        $(e.target).addClass('active');
    
        _href = $(e.target).attr('href');
        $('#text_groups div').fadeOut("fast");
        setTimeout("$(_href).fadeIn('fast')",400);
        
        return false;
    });
}


