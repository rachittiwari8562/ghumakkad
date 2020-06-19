$(document).ready(function() {
  $(".location").click(function(){
      if (navigator.geolocation)
      {
          navigator.geolocation.getCurrentPosition(successFunction,errorFunction);
      }
      else
      {
          alert('It seems like Geolocation, which is required for this page, is not enabled in your browser.');
      }
});
});
function successFunction(position)
{
    var lati = position.coords.latitude;
    var longi = position.coords.longitude;
    $("#latitude").val(lati);
    $("#longitude").val(longi);
    $("#myform").submit();
}
function errorFunction(position)
{
    alert('Error!');
}
