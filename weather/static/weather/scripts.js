$(function () {
  $("#city").autocomplete({
      source: function (request, response) {
          $.ajax({
              url: "/autocomplete/",
              data: {
                  term: request.term
              },
              success: function (data) {
                  const filteredLastSearches = lastSearches.filter(city =>
                      city.toLowerCase().startsWith(request.term.toLowerCase())
                  );
                  const suggestions = filteredLastSearches.concat(data);
                  response(suggestions);
              }
          });
      },
      minLength: 0,
      select: function (event, ui) {
          $("#city").val(ui.item.value);
          $("form").submit();
      },
  });

  $("#city").on('focus', function () {
      $(this).autocomplete("search", "");
  });
});