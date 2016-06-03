function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<li>';

        htmlString += '<a href="' + data.url + '">';
        htmlString += '<h2 class="title">' + data.title + '</h2>';
        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}
