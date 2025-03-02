function showsidebar() {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "flex";
}

function hidesidebar() {
  const sidebar = document.querySelector(".sidebar");
  sidebar.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.querySelector(".search-container input");
  if (searchInput) {
    function updatePlaceholder() {
      if (window.innerWidth < 500) {
        searchInput.placeholder = "Search";
      } else {
        searchInput.placeholder = "Search hotel, cities, etc.";
      }
    }
    updatePlaceholder();
    window.addEventListener("resize", updatePlaceholder);
  }
});




document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("search-btn"); // Assuming button has this ID
  const searchContainer = document.querySelector(".search-container");
  const cardsContainer = document.querySelector(".cards-container");

  searchBtn.addEventListener("click", function () {
    // Move search bar to top
    searchContainer.classList.add("movetotop");

    // render hotel-list

    // Show hotel list (animate from bottom)
    setTimeout(() => {
      cardsContainer.classList.add("show-cards");
    }, 500); // Delay to make animation smooth
  });
});




function display_hoetl_list(hotel_list) {
  $('#hotel-list').empty();


  if (!Array.isArray(hotel_list) || hotel_list.length === 0) {
    $('#hotel-list').append('<p>No hotels found.</p>');
    return;
  }
  // Flatten the nested array if needed
  let flattened_list = hotel_list.flat();

  flattened_list.forEach(element => {
    // console.log(element);
    let temp = `<div class="card mb-3" id="long-cards" style="max-width: 100%;">
                  <div class="row g-0">
                      <div class="col-md-4">
                          <img src="${element.hotel_images ? element.hotel_images[0] : ''}" class="img-fluid rounded-start" alt="card image"
                              style="background: grey;" loading="lazy">
                      </div>
                      <div class="col-md-8">
                          <div class="card-body">
                              <h5 class="card-title" style="font-size: 1.2rem;color: #444; font-weight: 600;">${element.hotel_name}</h5>
                              <p class="card-text"><small class="text-body-secondary">${element.location.city}, ${element.location.state}, ${element.location.country}</small></p>
                              <p class="card-text"><small class="text-body-secondary">⭐ ${element.rating}</small></p>
                              <p class="card-text">Services: <small class="text-body-secondary">${element.services}</small></p>
                              <p class="card-text">${element.description}</p>
                              <p class="card-text"><small class="text-body-primary"
                                      style="font-size: 1.5rem; font-weight: 300;">Price: ${element.base_price}/- <small style="font-size: 0.8rem; font-weight: 200;"> + GST</small></small></p>
                              <a href="/view/hotel/?hotel_id=${element._id}" class="btn btn-primary" "hotel_id"=${element._id}>Book</a>
                          </div>
                      </div>
                  </div>
              </div>`

    $('#hotel-list').append(temp);
  });
}

function search_hotel() {
  const search_query = $('#search_query').val();
  // if (search_query == "") {
  //   alert('Please enter the search query');
  // } else 
  {
    $.ajax({
      type: "POST",
      url: '/search/hotel',
      contentType: "application/json",
      data: JSON.stringify({
        data: {
          'search_query': search_query,
        },
        "role": "user",
      }),
      dataType: "json",
      success: function (response) {
        console.log(response)
        // alert(response['msg']);
        display_hoetl_list(response['hotel_list'])
      },
      error: function (response) {
        alert(response['responseJSON']['error']);
      }
    });
  }

}