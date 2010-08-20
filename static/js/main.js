(function() {

var eval_js = function(code) {
    try {
        $('#raphael_canvas').empty();
        eval(code);
    } catch (e) {
        console.error(e);
    }
};
$('#svg_canvas').html($('#svg textarea').val());

$('#svg textarea').bind('keyup change', function() {
    $('#svg_canvas').html(this.value);
});

$('#raphael textarea').bind('keyup change', function() {
    eval_js(this.value);
});

$('#to_raphael').click(function() {
    $.post('/convert', { svg: $('#svg textarea').val() }, function(data) {
        $('#raphael textarea').val(data);
        eval_js(data);
    });
});

})();
