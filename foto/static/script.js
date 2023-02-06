if (window.jQuery) {
  // jQuery подключен к странице
  console.log('jQuery подключен к странице')
}
else {
  console.log('jQuery НЕ подключен к странице')
}


function delete_comment(id) {
  $.ajax({
      type: $('#delete_form_'+id).attr('method'),
      url: $('#delete_form_'+id).attr('action'),
      data: $('#delete_form_'+id).serialize(),
      success: function (data) {
          $('#card_'+id).remove();
          // alert('Комментарий удален')
          location.reload();
          
      }
  });
}


for (let i = 0; i < 5; i++) {
  $('.info__add').click(function() {
    $(this).parent().append($('<div>', {
      'text': i
    }));
  });
}




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

