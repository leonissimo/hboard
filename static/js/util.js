function startRefreshIndoor(){
    setInterval(function () {
            $.ajax({
              url: '/current',
            })
            .done(function(data) {
              $('#temperature').text(data.temperature);
              $('#temperatureP').text(data.temperatureP);
              $('#pressure').text(data.pressure);
              $('#humidity').text(data.humidity);

            });
		}, 30*1000);
}