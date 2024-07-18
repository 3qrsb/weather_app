$(function () {
    $("#city").autocomplete({
      source: "/autocomplete/",
      minLength: 2,
      select: function (event, ui) {
        $("#city").val(ui.item.value);
      },
    });
  });