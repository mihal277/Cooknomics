function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        newElementsHtml.push('<li><a href="' + data.url + '"><h2 class="title">' + data.title + '</h2></a></li>');
    });
    console.log(newElementsHtml);
    $("#newslist-anchor").before(newElementsHtml.join(""));
}
