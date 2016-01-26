/**
 * Controller setup to receive status updates regarding a booking  
 */

var Mcrypt = require('mcrypt').MCrypt;
var webhookKey = 'abcdefgh12345678';

function decrypt(payload) {
    var base64Decoded = new Buffer(payload, 'base64');

    var initialVector = base64Decoded.toString('ascii', 0, 16);
    var aes = new Mcrypt('rijndael-128', 'cbc');

    var decipher = aes.open(webhookKey, initialVector);
    var decodedValue = aes.decrypt(base64Decoded.slice(16));
    var decodedPayload = decodedValue.toString('ascii');
    return JSON.parse(decodedPayload.substring(0, decodedPayload.indexOf('*')));
}

BookingWebhookController = {

    receive: function(req, res) {
        var payload = req.body != null ? req.body.payload : null;
        if (payload) {
            var bookingDetails = decrypt(payload);
            // Do stuff with the booking
            if (bookingDetails['new_booking_status']=='completed') {
                
            }
        }

    }

};
module.exports = BookingWebhookController;
