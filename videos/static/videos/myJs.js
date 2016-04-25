jQuery(document).ready(function(a) {
    var b = 1170;
    if (a(window).width() > b) {
        var c = a(".navbar-custom").height();
        a(window).on("scroll", {
            previousTop: 0
        }, function() {
            var b = a(window).scrollTop();
            b < this.previousTop ? b > 0 && a(".navbar-custom").hasClass("is-fixed") ? a(".navbar-custom").addClass("is-visible") : a(".navbar-custom").removeClass("is-visible is-fixed") : b > this.previousTop && (a(".navbar-custom").removeClass("is-visible"), b > c && !a(".navbar-custom").hasClass("is-fixed") && a(".navbar-custom").addClass("is-fixed")), this.previousTop = b
        })
    }
});