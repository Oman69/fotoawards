if (window.jQuery) {
  // jQuery подключен к странице
  console.log('jQuery подключен к странице')
}
else {
  console.log('jQuery НЕ подключен к странице')
}


document.getElementById('delete_comment').onclick = function() {
  let comment_id = $(this).attr('data-object-id');
  let url = `delete/${comment_id}/`;
  $.ajax({
    type: 'DELETE',
    url: '/delete/',
    dataType: 'json',
    data: {
      'csrfmiddlewaretoken': "{{ csrf_token }}"
  },
    }).done(
      function(){alert("Deleted");}).fail(function(){alert("Error");}
    ) 
  };


/*
let csrftoken = '{{ csrf_token }}'

document.getElementById('delete_comment').onclick = function(e) {
  e.preventDefault();
  const requestObj = new XMLHttpRequest()
  requestObj.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText)
    }
  }

  
  requestObj.open("DELETE", '/delete/')

  const formdata = new FormData()

  formdata.append('name', 'John')
  formdata.append('age', '17')

  requestObj.send(formdata)
}; */



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

