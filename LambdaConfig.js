'use strict';
var AWS = require('aws-sdk');
AWS.config.update({region: 'us-west-2'});
var iotdata = new AWS.IotData({endpoint: 'a2wvihqic469dv.iot.us-west-2.amazonaws.com'});


console.log('Loading function');

var globalThreashold = 50;

exports.handler = (event, context, callback) => {
    //console.log('Received event:', JSON.stringify(event, null, 2));
    console.log('Sensor read from side  :', event.sensor_side);
    console.log('Sensor value :', event.sensor_value);
    console.log('globalThreashold Sensor value :', globalThreashold);
    
    var sensorSide = event.sensor_side;
    var sensorValue = event.sensor_value;
    if(sensorValue <= globalThreashold ){
        console.log('Sensor reached threashold on side  :', sensorSide);
        
        var params = {
        topic: 'Gesture-Pi/Commands',
        payload: "Stop",
        qos: 1
        };
        
     
        iotdata.publish(params, function(err, data){
            if(err){
                console.log(err);
            }
            else{
                console.log("success?");
                //context.succeed(event);
            }
        });
        
    }
   callback(null, "Done Processing");  // Echo back the first key value
    //callback('Something went wrong');
    
    
};
