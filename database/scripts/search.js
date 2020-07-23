let s_engine = new MiniSearch({
    fields: ['Name', 'Code', 'Set', 'Regulator', 'Lab', 'Publication', 'Keywords'],
    storeFields: ['Name', 'Code', 'Keywords'],
    searchOptions: {
      prefix: true,
      fuzzy: 0.2
    }
})

s_engine.addAll (parts)

var s_bar = document.getElementById("search-input");

s_bar.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("search-btn").click();
  }
}); 


function launch_search(){
    var query = document.getElementById('search-input').value
    let res = s_engine.search(query)
    document.getElementById('results').innerHTML = `<p><strong>Query</strong>: ${query}</p>`
    setTimeout(function(){
      if (res && res.length){
        res.forEach(function(part){
          document.getElementById('results').innerHTML += `<li><a href='../parts/${part.Code}.html'>${part.Name} ${part.Code}</a><p>Keywords: ${part.Keywords}</p></li>`
        })
      } else {
        document.getElementById('results').innerHTML += '<li><p>No parts found... Try browsing the Catalogue or read the Help file for instructions in searching.</p></li>'
      }
    }, 100)
}