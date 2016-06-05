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

function appendElements(newData) {
    var newElementsHtml = [];
    $.each(newData, function(element, data) {
        var htmlString = '<div class="article-list-single">';

        htmlString += '<a href="' + data.url + '">';
        htmlString += '<h2>' + data.title + '</h2></a>';
        htmlString += trim_str_to_n(data.content, 150);
        htmlString += '<a href="' + data.url + '">' + 'Go to article</a>';
        htmlString += '<p>Posted by ' + data.author + 'on ' + data.published_date + '</p>';
        htmlString += '</a>';
        htmlString += '</div>';

        newElementsHtml.push(htmlString);
    });
    $(".element-list").append(newElementsHtml.join(""));
}
