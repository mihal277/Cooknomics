function loadPageOnScrollAndNavbar() {
    loadPageOnScroll();
    fancyNavbar();
}

function fancyNavbar() {
    var b = 1170;
    if ($(window).width() > b) {
        var navbarCustom = $(".navbar-custom");
        var c = navbarCustom.height();
        $(window).on("scroll", {
            previousTop: 0
        }, function() {
            var b = $(window).scrollTop();

            b < this.previousTop ? b > 0 && navbarCustom.hasClass("is-fixed") ? navbarCustom.addClass(
                "is-visible") : navbarCustom.removeClass("is-visible is-fixed") : b > this.previousTop && (navbarCustom
                .removeClass("is-visible"), b > c && !navbarCustom.hasClass("is-fixed") && navbarCustom.addClass(
                "is-fixed")), this.previousTop = b
        })
    }
}

function loadPageOnScroll() {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        // turn of the event handler so it doest't fire again
        $(window).off('scroll');
        loadPage(null);
    }
}

function loadPage(errorHandler) {
    if (hasNextPage == false) {
        return false;
    }

    pageNumber++;

    var formData = {
        page: pageNumber
    };

    /* Create a dict to send to server (dicts are easier to use there), if
     * the request is going to ask for filtered results. */
    if (dataDict != null) {
        for (var key in dataDict) {
             if (dataDict.hasOwnProperty(key)) {
                formData[key] = ''
            }
        }
    }

    $.ajax({
        type: 'GET',
        url: url,
        data: formData,
        dataType: 'json',
        encode: true
    })
    .done(function(data) {
        hasNextPage = data.page.has_next;
        var newPage = data.page.objects;
        appendElements(newPage);

        $(window).on('scroll', loadPageOnScrollAndNavbar);
    })
    .error(function(jqXHR) {
        console.log(jqXHR.status);

        if (typeof errorHandler == 'function') {
            errorHandler(jqXHR.status);
        }
    });
}

$(document).ready(function() {
    $(window).on('scroll', loadPageOnScrollAndNavbar);
});