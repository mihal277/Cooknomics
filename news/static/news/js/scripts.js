/*
   Appends data fetched from server to the list of elements on webstie.
   Gets called when user scrolls down the page and AJAX request to fetch
   new data is finished.
 */
function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<li>';

        htmlString += '<a href="' + data.url + '">';
        htmlString += '<h2 class="title">' + data.title + '</h2>';
        htmlString += '<div class="video_buttons row">';
        htmlString += '<button class="upvote-button" name="' + element + '" id="upbtn_' + element + '"' +
            ' data-on-click-action="upvote">';
        htmlString += '<i class="fa fa-thumbs-up fa-lg"></i>';
        htmlString += '<section id="upvote_count_' + element + '">' + data.up_votes + '</section>';
        htmlString += '</button>';
        htmlString += '<button class="downvote-button" name="' + element + '" id="dwnbtn_'+ element + '"' +
                                'data-on-click-action="downvote">';
        htmlString += '<i class="fa fa-thumbs-down fa-lg"></i>';
        htmlString += '<section id="downvote_count_'+ element +'">' + data.down_votes +'</section>';
        htmlString += '</button>';
        htmlString += '</div>';
        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}
