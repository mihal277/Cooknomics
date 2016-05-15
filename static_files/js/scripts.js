function loadPageOnScroll() {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        // turn of the event handler so it doest't fire again
        $(window).off('scroll');
        loadPage();
    }
}

function loadPage() {
    if (hasNextPage == false) {
        return false;
    }

    pageNumber++;
    var formData = {
        'page': pageNumber
    };

    $.ajax({
        type: 'GET',
        url: url,
        data: formData,
        dataType: 'json'
    })
    .done(function(data) {
        hasNextPage = data.page.has_next;
        var newPage = data.page.objects;

        appendElements(newPage);

        $(window).on('scroll', loadPageOnScroll)
    })
    .error(function(jqXHR) {
        console.log(jqXHR.status)
    });
}

$(document).ready(function() {
    $(window).on('scroll', loadPageOnScroll);
});