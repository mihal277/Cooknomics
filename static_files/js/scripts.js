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

/*
   When user scrolls down the page, calls the function that fetches new data
   form server. In most cases it passes no data to loadPage function, meaning that
   there is no callback function on ajax error.
 */
function loadPageOnScroll() {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        // turn of the event handler so it doest't fire again
        $(window).off('scroll');
        loadPage();
    }
}

/*
    Loads new page from the server. Uses global variables that are declared in
    every template that has pagination:
        - pageNumber: number of the that is going to be fetched from server
        - hasNextPage: sets the variable depending on whether there is new page
          that can be fetched from server
        - dataDict: if the dictionary is null it means that no filterig arguments
          are going to be sent to the server. If it is not null it creates dictionary
          of elements that are going to be used as filters on the server (e.g ingredients
          when serching for recipes).
    If errorHandler is defined, when AJAX error occurs errorHandler is call with server
    response status code.
 */
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
                formData[key] = dataDict[key];
            }
        }
    }
    /* Add sorting parameter to data sent to server. */
    formData['sorting'] = currentSorting;

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

/* Adds event listener to scroll function. */
$(document).ready(function() {
    $(window).on('scroll', loadPageOnScrollAndNavbar);
});
