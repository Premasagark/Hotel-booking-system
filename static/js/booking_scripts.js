window.addEventListener("load", () => {
  const roomOptions = document.querySelectorAll(".room-option");

  roomOptions.forEach((option) => {
    option.addEventListener("click", handleSelectorClick);
  });
});

const handleSelectorClick = (e) => {
  // Remove grow effect from all labels first
  document.querySelectorAll(".room-selector label").forEach((label) => {
    label.style.flex = "1"; // Reset to default size

  });

  // Grow the clicked label
  e.target.style.flex = "1.5";
};


$(document).ready(function () {

  let hotel = $("#hotel_details").attr("hotel_id");;
  console.log("Hotel ID:", hotel);

  $.ajax({
    type: "post",
    url: "/search/view/hotel",
    data: JSON.stringify({ hotel_id: hotel }),
    dataType: "json",
    contentType: "application/json",
    success: function (response) {
      console.log(response['hotel']);
      display_hoetl_details(response['hotel']);
    },
    error: function (response) {
      console.log(response['responseJSON']['error']);
    },
  });
});


function display_hoetl_details(hotel) {
  // Populate hotel details
  $("#hotel_details").text(hotel.hotel_name);
  $(".details-container h2").text(hotel.hotel_name);
  $(".details-container p:first").html(`📍 ${hotel.address}`);
  $(".details-container p:nth-child(3)").text(hotel.description);

  // Populate services
  let servicesHtml = '';
  hotel.services.forEach(function (service) {
    servicesHtml += `<div class="col">${service}</div>`;
  });
  $(".service .row").html(servicesHtml);

  // Populate room types
  let roomTypesHtml = '';
  hotel.room_types.forEach(function (roomType) {
    roomTypesHtml += `
      <div class="room-option">
        <input type="radio" name="room" id="${roomType.room_type_id}" value="${roomType.room_type_id}">
        <label for="${roomType.room_type_id}" title="${roomType.room_type_name} - ₹${roomType.room_type_price}">
          ${roomType.room_type_name} (₹${roomType.room_type_price})
        </label>
      </div>
    `;
  });
  $(".room-selector").html(roomTypesHtml);


  hotel.hotel_images.forEach((element, index) => {
    let imagetemp = `<div class="carousel-item ${index === 0 ? 'active' : ''}">
                        <img src="${element}" class="d-block w-100" alt="...">
                    </div>`
    $('.carousel-inner').append(imagetemp);

    let imagebutton = `<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="${index}"
                        aria-label="Slide ${index + 1}" ${index === 0 ? 'class="active"' : ''}></button>`

    $('.carousel-indicators').append(imagebutton);

  });
}

function collectdata() {
  var formData = {
    name: $('input[aria-label="First name"]').val(),
    phone_number: $('input[aria-label="phoneno"]').val(),
    booking_email: $('input[aria-label="email"]').val(),
    checkin: $('#checkin').val(),
    checkout: $('#checkout').val(),
    adults: parseInt($('select[aria-label="Default select example"]').eq(0).val()),
    children: parseInt($('select[aria-label="Default select example"]').eq(1).val()),
    rooms: parseInt($('select[aria-label="Default select example"]').eq(2).val()),
    room_type: {
      room_type_id: parseInt($('input[name="room"]:checked').attr('id')),
      room_type_name: $('input[name="room"]:checked').next('label').attr('title')
    },
    hotel_id: $('#hotel_details').attr('hotel_id'),
  };
  console.log(formData);

  $.ajax({
    type: 'post',
    url: '/booking/room/',
    data: JSON.stringify(formData),
    dataType: 'json',
    contentType: 'application/json',
    success: function (response) {
      alert('Booking successful!');
      window.location.replace('/home');
    },
    error: function (error) {
      alert('Booking failed!');

    }
  });
}