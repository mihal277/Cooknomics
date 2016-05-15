function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<li>';
        htmlString += '<a href="' + data.url + '"><h2 class="title">' + data.title + '</h2></a>';
        htmlString += '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + data.video_url + '" frameborder="0" allowfullscreen></iframe>'
        htmlString += '</li>';

        newElementsHtml.push(htmlString);
    });
    console.log(newElementsHtml);
    $("#videolist-anchor").before(newElementsHtml.join(""));
}