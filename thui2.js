function randomData() {
    now = new Date(+now + oneDay);
    value = value + Math.random() * 21 - 10;
    return {
        name: now.toString(),
        value: [
            Math.round(value)
        ]
    }
}

var dataTHUI2 = [];
var dataI2CST = [];
var dataCSTTHU = [];
var now = +new Date(1997, 9, 3);
var oneDay = 24 * 3600 * 1000;
var value = Math.random() * 1000;
for (var i = 0; i < 10; i++) {
	dataCSTTHU.push(Math.round(15));
	dataTHUI2.push(Math.round(20));
	dataI2CST.push(Math.round(10));
}
var timeData = (function (){  
		var now = new Date();
		var res = [];
		var len = 10;
		while (len--) {
    			res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
    			now = new Date(now - 2000);
		}
		return res;
})();

optTHUI2 = {
    backgroundColor: '#fff',
    tooltip:{
	    trigger: 'axis',
	    formatter: function (params) {
		    var str=''
		    params.forEach(function(item,i){
			    str += item.name + '<br/>'
		    + item.seriesName + ' : ' + item.value + 'KB/s<br/>'; 
		    });

		    return str         },
	    axisPointer: { 
	 	    animation: false
	    }
    },
   legend:{
	show:true,
        x:'left',
	data:['THU--I2','I2--CST','CST--THU'],
        textStyle: {
            color: '#000'
        },
        selectedMode: 'multiple'
    },
    xAxis: {
        type: 'category',
        splitLine: {
            show: false
        },
	data:timeData
    },
    yAxis: {
	name:'流量(KB/s)',
        type: 'value',
        boundaryGap: [0, '100%'],
        splitLine: {
            show:true
        }
    },
    series: [{
        name: 'THU--I2',
        type: 'line',
        showSymbol: false,
        hoverAnimation: false,
        data: dataTHUI2
    },{
        name: 'I2--CST',
        type: 'line',
        showSymbol: false,
        hoverAnimation: false,
        data: dataI2CST
    },{
        name: 'CST--THU',
        type: 'line',
        showSymbol: false,
        hoverAnimation: false,
        data: dataCSTTHU
    }

    ]
};

