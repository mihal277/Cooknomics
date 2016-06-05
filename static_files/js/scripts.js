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

/* Function that send up/down vote request to server and updates
   up/down vote count with data recieved from server.
 */
function postVote(event) {
    var action = $(this).data('on-click-action');
    var pk = $(this).attr('name');

    console.log("action: " + action);
    console.log(event.data.voteUrl);

    var postData = {
        pk: pk,
        type: action
    };

    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        url: event.data.voteUrl,
        data: postData,
        dataType: 'json',
        encode: true
    })
    .done(function(data) {
        $('#upvote_count_' + pk).html(data.upvotes);
        $('#downvote_count_' + pk).html(data.downvotes);
    })
    .error(function(jqXHR) {
        console.log(jqXHR.status);
    })
}

/* Utility functions */

/* get CSRF token from cookie, copied from https://docs.djangoproject.com/en/1.9/ref/csrf/ */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
