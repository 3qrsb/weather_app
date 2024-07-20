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

$(document).ready(function () {
    $('#searchHistoryModal').on('show.bs.modal', function () {
      $.ajax({
        url: '/search-count/',
        method: 'GET',
        success: function (data) {
          const searchHistoryList = $('#searchHistoryList');
          searchHistoryList.empty();
  
          data.forEach(function (item) {
            searchHistoryList.append(`<li class="list-group-item">${item.city} - ${item.count} searches</li>`);
          });
        },
        error: function () {
          alert('Failed to fetch search history');
        }
      });
    });
  });