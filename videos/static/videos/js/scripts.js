/*
   Appends data fetched from server to the list of elements on webstie.
   Gets called when user scrolls down the page and AJAX request to fetch
   new data is finished.
 */
function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<li>';
        htmlString += '<a href="' + data.url + '"><h2 class="title">' + data.title + '</h2></a>';
        htmlString += '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + data.video_url +
            '" frameborder="0" allowfullscreen></iframe>';

        /* Updating likes part */
        var upvote_class = 'upvote-button fa fa-thumbs-up fa-lg';
        var downvote_class = 'downvote-button fa fa-thumbs-down fa-lg';

        console.log(data.voting_status);
        if (data.voting_status == 'upvoted') {
            upvote_class += ' clicked';
        }
        if (data.voting_status == 'downvoted') {
            downvote_class = ' clicked';
        }

        htmlString += '<div class="video_buttons row">';
        htmlString += '<i class="' + upvote_class +'" name="' + data.slug + '" id="upbtn_' + data.slug + '"' +
            ' data-on-click-action="upvote"></i>';
        htmlString += '<section id="upvote_count_' + data.slug + '">' + data.up_votes + '</section>';

        htmlString += '<i class="' + downvote_class + '" name="' + data.slug + '" id="dwnbtn_'+ data.slug + '"' +
                                'data-on-click-action="downvote"></i>';
        htmlString += '<section id="downvote_count_'+ data.slug +'">' + data.down_votes +'</section>';
        htmlString += '</div>';
        /* End of updating likes */


        htmlString += '</li>';
        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}