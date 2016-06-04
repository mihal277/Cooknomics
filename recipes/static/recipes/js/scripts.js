function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<li>';

        htmlString += '<a href="' + data.url + '"><h2 class="title">' + data.title + '</h2></a>';
        htmlString += '<img src="' + data.image_url + '" style="max-height:315px;width:auto;">';
        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    console.log(newElementsHtml);
    $(".element-list").append(newElementsHtml.join(""));
}