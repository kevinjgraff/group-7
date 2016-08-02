  $.getJSON('http://en.wikipedia.org/w/api.php?action=parse&page=google&prop=text&format=json&callback=?', function(json) { 
    $("#information").html(json.parse(text['*'])); 
    $("#information").find("a:not(.references a)").attr("href", function(){ return "http://www.wikipedia.org" + $(this).attr("href");}); 
    $("#information").find("a").attr("target", "_blank"); 
