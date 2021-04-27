$("form[name=signup_form").submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $ajax({
    URL: "/signform",
    type: "POST",
    data: data,
    dataType: "json",
    success: function (resp) {
      console.log(resp);
    },
    error: function (resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    },
  });
  e.preventDefault();
});
