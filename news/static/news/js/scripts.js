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
        var date = new Date(data.published_date)
        htmlString += '<div class="post">';
        htmlString += '<a href="' + data.url + '"><h2>' + data.title + '</h2></a>';
        
        htmlString += '<i class="fa fa-clock-o footnote-icon" aria-hidden="true"></i>' +
                      '<p class="post-metadata"> ' + date + '</p>';
        htmlString += '<i class="fa fa-comment comment-icon" aria-hidden="true"></i>' +
                      '<a href="' + data.url + '#disqus_thread" class="comment-link"></a>';


        var upvote_class = 'fa fa-thumbs-up fa-lg upvote-button';
        var downvote_class = 'fa fa-thumbs-down fa-lg downvote-button';
        if (data.voting_status == 'upvoted') {
            upvote_class += ' clicked';
        }
        if (data.voting_status == 'downvoted') {
            downvote_class = ' clicked';
        }

        htmlString += '<div class="like-buttons">';
        htmlString += '<i class="' + upvote_class +'" data-name="' + data.slug + '" id="upbtn_' + data.slug + '"' +
            ' data-on-click-action="upvote"></i>';
        htmlString += '<section id="upvote_count_' + data.slug + '" class="votes-count">' + data.up_votes + '</section>';

        htmlString += '<i class="' + downvote_class + '" data-name="' + data.slug + '" id="dwnbtn_'+ data.slug + '"' +
                                'data-on-click-action="downvote"></i>';
        htmlString += '<section id="downvote_count_'+ data.slug +'" class="votes-count">' + data.down_votes +'</section>';
        htmlString += '</div>';


        htmlString += '<p class="short-content">' + data.shortened_content + '</p>';
        htmlString += '<a href="' + data.url + '" class="button">Read and comment</a>';
        htmlString += '</div>';

        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}

