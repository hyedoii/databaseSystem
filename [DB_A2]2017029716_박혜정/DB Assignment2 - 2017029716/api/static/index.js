$(document).ready(() => {

  $("#position").submit((e) => {
    e.preventDefault()
    console.log("모야")
    console.dir(e.target.lat.value)
    console.log(typeof e.target.lat.value)
  })

  $("#here").click(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        console.log(position.coords.latitude)
        console.log(position.coords.longitude)
      });
    } else {
      x.innerHTML = "Geolocation is not supported by this browser.";
    }
  })

  $("#btnAdd").click(function () {


  })
})

