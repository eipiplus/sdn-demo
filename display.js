var geoCoordMap = {
    'THU': [-110,115.4746],
    'BUPT': [-120.4651,131.3373],
    'CST': [-95.4778,140.0951],
    'I2': [100.4651,126.3373],
};
var pointData = {
	thu:{name:'THU',value:[2]},
	i2:{name:'I2',value:[1]},
	cst:{name:'CST',value:[1]}
};
var linkData = [
    [pointData.i2,  pointData.thu, pointData.thu],
    [pointData.i2,  pointData.cst, pointData.i2],
    [pointData.cst, pointData.thu, pointData.cst]
];
var routeData = [
	["Route Policy",
	[[pointData.i2,pointData.thu]],6]
];
var rerouteData = [
	["ReRoute Policy",
	[[pointData.i2,pointData.cst],[pointData.cst,pointData.thu]],6]
];

function convertPoint(data){
    var res = [];
    for (var i = 0; i < data.length; i++) {
		    var geoCoord = geoCoordMap[data[i].name];
		    if (geoCoord) {
			    res.push({
				    name: data[i].name,
				    value: data[i].value
			    });
		    }
    }
	return res;
}
var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var dataItem = data[i];
        var fromCoord = geoCoordMap[dataItem[0].name];
        var toCoord = geoCoordMap[dataItem[1].name];
        if (fromCoord && toCoord) {
            res.push([{
                coord: fromCoord
            }, {
                coord: toCoord
            }]);
        }
    }
    return res;
};
var color = ['#a6c84c', '#ffa022', '#46bee9'];
var series = [];
function pushdata(series,list){
	list.forEach(function (item, i) {
	    series.push(
	  /*,*/
	    {
		name: item[0],
		type: 'lines',
		zlevel: 1,
		effect: {
		    show:false, 
		    period: 6,
		    trailLength: 0,
		    symbolSize: 15
		},
		lineStyle: {
		    normal: {
			color: color[0],
				width: 2,
				opacity: 0.4,
			curveness: 0.2
		    }
		},
		data: convertData(item[1])
	    },
    {
        name: item[0] ,
        type: 'effectScatter',
        coordinateSystem: 'geo',
        zlevel: 2,
        rippleEffect: {
            brushType: 'stroke'
        },
        label: {
            normal: {
                show: true,
                position: 'right',
                formatter: '{b}'
            }
        },
        symbolSize: 10,
        itemStyle: {
            normal: {
                color: color[1]
            }
        },
	markPoint:{
		symbolSize:30,	
		label:{
			normal:{
				show:true,
				position:'right',
				formatter:'{b}'
			}
		},
		data: item[1].map(function (dataItem) {
		    return {
			name: dataItem[2].name,
			value:dataItem[2].value,
			coord:geoCoordMap[dataItem[2].name]
		    };
		})
	}
    }
	);
	})
};
function addroute(series,list){
	list.forEach(function(item,i){
		series.push(
		{
		name: item[0] + ' Route',
		type: 'lines',
		zlevel: 1,
		effect: {
		    show: true,
		    period: item[2],
		    trailLength: 0.7,
		    color: '#fff',
		    symbolSize: 5
		},
		lineStyle: {
		    normal: {
			color: color[i],
			width: 0,
			curveness: 0.2
		    }
		},
		data: convertData(item[1])
	    })
}
		
)
	
};
pushdata(series,[['Total Routers',linkData]]);
var serl=series.length;
addroute(series,routeData);
option = {
    backgroundColor: '#404a59',
    tooltip : {
        trigger: 'item'
    },
    legend: {
	show:false,
        orient: 'vertical',
        top: 'bottom',
        left: 'right',
        data:['Domain'],
        textStyle: {
            color: '#fff'
        },
        selectedMode: 'single'
    },
    geo: {
        map: 'worldsp',
        label: {
            emphasis: {
                show: false
            }
        },
        roam: true,
	itemStyle: {
            normal: {
                areaColor: '#323c48',
                borderColor: '#404a59'
            },
            emphasis: {
                areaColor: '#2a333d'
            }
        }
    },
    series: series
};
