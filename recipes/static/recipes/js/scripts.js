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
        htmlString += '<img src="' + data.image_url + '" style="max-height:315px;width:auto;">';
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
        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}

/*
   Fetches all ingredients from server and appends them
   to a select box.

   :param requestUrl: URL on server that responds to the request.
 */
function fillIngredientSelectBox(requestUrl) {
    var $productList = $('#ingredient-selecter');

    $.ajax({
        type: 'GET',
        url: requestUrl
    })
    .done(function(data) {
        console.log(data);
        $.each(data, function(index, parameter) {
            $.each(parameter, function(name, value) {
                $productList.append('<option value="' + value + '">' + name + '</option>');
            });
        })
    })
    .error(function(jqXHR) {
        console.log("AJAX error: " + jqXHR.status);
    });
}

/*
   Gets called when user clicks search button.
   Sets global variables url and dataDict depending on ingredients
   selected by user and pageNumber and hasNextPage to 0/true, cause
   we expect some data back from server (see loadPage).
   Displays error message when server responds with error.

    :param: event: event.data should contain 2 urls:
                   - nonFilteredRecipesUrl - URL that responds with all recipes
                   - filteredRecipesUrl - URL that responds with recipes
                     filtered by ingredeients selected by user
 */
function loadNewPage(event) {
    var $errorMsg = $('#error-message');
    var $productList = $('#ingredient-selecter');
    var selectedItems = $productList.val();
    var $initalList = $('.element-list');

    $("#text-search").val(""); /* Clean search textbox */
    $errorMsg.hide();
    $initalList.empty();
    if (selectedItems == null) {
        /* If no items selected ask for all recipes */
        url = event.data.nonFilteredRecipesUrl;
        dataDict = null;
    } else {
        /* If some items selected ask for filtered recipes */
        url = event.data.filteredRecipesUrl;

        /* Create dict to send to server (its easier to process then) */
        var selectedItemsDict = {};
        var selectedItemsLength = selectedItems.length;
        for (var i = 0; i < selectedItemsLength; ++i) {
            selectedItemsDict[selectedItems[i]] = '';
        }
        dataDict = selectedItemsDict;
    }

    /* 0, cause loadPage does pageNumber++ */
    pageNumber = 0;
    hasNextPage = true;

    loadPage(function(errorStatus) {
        var $errorMsg = $('#error-message');

        if (errorStatus == 404) {
            $errorMsg.text("Nie znaleziono żadnych przepisów.");
            $errorMsg.css('display', 'table');
        }
    })
}