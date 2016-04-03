

function gauge() {

		gauge = new Highcharts.Chart({
			  chart: {
				  renderTo : 'container',
		            type: 'gauge',
		            plotBackgroundColor: null,
		            plotBackgroundImage: null,
		            plotBorderWidth: 0,
		            plotShadow: false
		        },

		        title: {
		            text: 'Indoor Temperature'
		        },

		        pane: {
		            startAngle: -140,
		            endAngle: 140,
		            background: [{
		                backgroundColor: {
		                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
		                    stops: [
		                        [0, '#FFF'],
		                        [1, '#333']
		                    ]
		                },
		                borderWidth: 0,
		                outerRadius: '109%'
		            }, {
		                backgroundColor: {
		                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
		                    stops: [
		                        [0, '#333'],
		                        [1, '#FFF']
		                    ]
		                },
		                borderWidth: 1,
		                outerRadius: '107%'
		            }, {
		                // default background
		            }, {
		                backgroundColor: '#DDD',
		                borderWidth: 0,
		                outerRadius: '105%',
		                innerRadius: '103%'
		            }]
		        },

		        // the value axis
		        yAxis: {
		            min: -5,
		            max: 40,

		            minorTickInterval: 'auto',
		            minorTickWidth: 1,
		            minorTickLength: 10,
		            minorTickPosition: 'inside',
		            minorTickColor: '#666',

		            tickPixelInterval: 30,
		            tickWidth: 2,
		            tickPosition: 'inside',
		            tickLength: 10,
		            tickColor: '#666',
		            labels: {
		                step: 2,
		                rotation: 'auto'
		            },
		            title: {
		                text: 'Celsius'
		            },
		            plotBands: [{
		                from: -10,
		                to: 10,
		                color: 'blue'
		            }, {
		                from: 10,
		                to: 25,
		                color: 'green'
		            }, {
		                from: 25,
		                to: 50,
		                color: '#DF5353' // red
		            }]
		        },

		        series: [{
		            name: 'Temperature',
		            data: [parseFloat(initData.temperature)],
		        }]
        });

         setInterval(function () {
            $.ajax({
              url: '/temp',
            })
            .done(function(data) {
              var point = gauge.series[0].points[0];
              point.update(parseFloat(data.temperature));
            });




        }, 10*1000);


};