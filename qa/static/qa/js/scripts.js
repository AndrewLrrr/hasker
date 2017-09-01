function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('.vote').click(function (e) {
    e.preventDefault();
    var url = $(this).attr('href');
    var $rating = $(this).parent().find('.rating');
    $.post(url, {
        'csrfmiddlewaretoken': getCookie('csrftoken')
    }, function (response) {
        $rating.text(response['rating']);
    });
});
