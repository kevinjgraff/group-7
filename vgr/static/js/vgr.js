  $(.getJSON('https://en.wikipedia.org/w/api.php?action=query&titles=Main%20Page&prop=revisions&rvprop=content&format=json&callback=?', 
    function(json) { 
    $("#information").html(json.parse(text['*'])); 
    $("#information").find("a:not(.references a)").attr("href",
    function(){ return "http://www.wikipedia.org" + $(this).attr("href");}); 
    $("#information").find("a").attr("target", "_blank"); });
 
 //$(.getJSON("http://en.wikipedia.org/w/api.php?action=parse&format=json&callback=?", {page:pageName, prop:"text"}, wikipediaHTMLResult);)

  function something(){
	window.location.replace('/results')
  }


  function setup(){
	$('#submit').click(something)
  }

  $(document).ready(setup)