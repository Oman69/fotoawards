console.log('Hello')
document.getElementById('delete_comment').onclick = function() {
  let requestObj = new XMLHttpRequest()
  requestObj.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText)
    }
  }
  requestObj.open("GET", './')
  requestObj.send()
};



if(get('ordering'))
  document.getElementById('placeholder').innerHTML = "Sort: " + document.getElementById(get('ordering')).innerHTML;

  function finalurl() {
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('ordering', document.getElementById("sort-list").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    return new_url
  };




if(get('filtering'))
  document.getElementById('placeholder').innerHTML = "Sort: " + document.getElementById(get('filtering')).innerHTML;

  function finalurl2() {
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('filtering', document.getElementById("filtering").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    return new_url
  };



if(get('user'))
  document.getElementById('placeholder').innerHTML = document.getElementById(get('user')).innerHTML;

  function finalurl3() {
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('user', document.getElementById("user-list").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    return new_url
  };

