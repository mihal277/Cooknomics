/*
   Appends data fetched from server to the list of elements on webstie.
   Gets called when user scrolls down the page and AJAX request to fetch
   new data is finished.
 */
function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        console.log("element = " + element + ", data = " + data);
        console.log("data.slug = " + data.slug);
        console.log("data.up_votes = " + data.up_votes);
        var htmlString = '<li>';

        htmlString += '<a href="' + data.url + '">';
        htmlString += '<h2 class="title">' + data.title + '</h2>';
        htmlString += '</a>';

        /* Updating likes part */
        htmlString += '<div class="video_buttons row">';
        htmlString += '<button class="upvote-button" name="' + data.slug + '" id="upbtn_' + data.slug + '"' +
            ' data-on-click-action="upvote">';
        htmlString += '<i class="fa fa-thumbs-up fa-lg"></i>';
        htmlString += '<section id="upvote_count_' + data.slug + '">' + data.up_votes + '</section>';
        htmlString += '</button>';
        htmlString += '<button class="downvote-button" name="' + data.slug + '" id="dwnbtn_'+ data.slug + '"' +
                                'data-on-click-action="downvote">';
        htmlString += '<i class="fa fa-thumbs-down fa-lg"></i>';
        htmlString += '<section id="downvote_count_'+ data.slug +'">' + data.down_votes +'</section>';
        htmlString += '</button>';
        htmlString += '</div>';
        /* End of updating likes */

        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}

function trim_str_to_n(str, n) {
    if (str.length > n) {
        var white_space_index = str.substring(n).indexOf(' ');
        if (!white_space_index)
            return str;
        return (str.substring(0, white_space_index) + "...");
    }
    else {
        return str;
    }
}
