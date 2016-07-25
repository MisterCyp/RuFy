var torrentStream = require('torrent-stream');
var rootPath = process.cwd();
var fs = require('fs');
var mkdirp = require('mkdirp');

var BITTORENT_PORT = 6881;

var appRouter = function(app) {

    app.post("/streamtorrent", function(req, res) {
        if(!req.body.magnet){
	    return res.send({"status": "error", "message": "missing magnet URI"});
        } else {
 	    var magnetURI = req.body.magnet;
            var engine = torrentStream(magnetURI);            
	    
      	    engine.on('ready', function() {
		engine.files.forEach(function(file) {
		    var fileName = file.name;
	 	    var filePath = file.path;
		    console.log(fileName + ' - ' + filePath);

		    mkdirp(rootPath + '/assets/videos/' + fileName, function(err) {
		        if (err) {
			    console.log(err);
			} else {
			    var videoPath = rootPath + '/assets/videos/' + fileName + '/video.mp4';
			    var writer = fs.createWriteStream(videoPath);
			    var videoSent = false;

			    stream.on('data', function(data) {
				writer.write(data);
				if(!videoSent) {
				    fs.exists(videoPath, function(exists) {
					if(exists) {
					    sails.sockets.broadcast(req.param('room'), 'video_ready', {videoPath : '/videos/' + fileName + '/video.mp4'});
					    videoSent = true;
					}
				    });
				}
			    });
			}
		    });
		});
	    });

	res.json({status: 'downloading'});
    }






    });


}
 
module.exports = appRouter;
