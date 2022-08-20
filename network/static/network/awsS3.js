const AWS = require('aws-sdk')

const s3 = new AWS.S3()
AWS.config.update({accessKeyId: 'AKIAZHCVDPUKBB2LK6WD', secretAccessKey: '8xNMFBJSZhd50AjzK9d2c+LfNBdk5sDNsTGa0DYs'})

const myBucket = 'django-greensky-bucket'
const myKey = 'images/a.jpeg'
const signedUrlExpireSeconds = 60 * 5 // your expiry time in seconds.

const url = s3.getSignedUrl('getObject', {
 Bucket: myBucket,
 Key: myKey,
 Expires: signedUrlExpireSeconds
})

// return the url to client
function download(url){
    $('<iframe>', { id:'idown', src:url }).hide().appendTo('body').click();
}
$("#downloadButton").click(function(){
    $.ajax({
        url: 'example.com/your_end_point',
        success: function(url){
            download(url);
        }
    })
});