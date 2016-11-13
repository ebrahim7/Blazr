var express = require('express');
var router = express.Router();
var request = require("request");

router.post ('/', function (req, res, next) {
	
	console.log('Search term: '+req.body.searchterm)
	console.log('Search term; '+req.query.searchterm)

    var options = { method: 'GET',
        url: 'https://jobs.github.com/positions.json',
        qs:{ 
            description: req.body.searchterm,
        headers:
        { 'postman-token': 'ea90e0ac-7c80-e2a4-ab57-3025cc142381',
			'cache-control': 'no-cache' }  } };

    request(options, function (error, response, body) {
        if (error) throw new Error(error);

        //console.log(body);

        var searchterm = req.body.searchterm;
		console.log(req);
        //res.send({searchterm: searchterm, body: body});
		
		var json_body = JSON.parse(body)
		var jobs_results = json_body //give all the results to the jobs_results object
		
		/*for (var i = 0; i < json_body.length; i++){
			//var job_title = json_body[i].title;
			var job_created_at = json_body[i].created_at;
			var job_location = json_body[i].location;
			jobs_results = json_body[i]
		}*/
		
		//res.send(titles);
		res.render('jobs', { jobs: jobs_results }); //give jobs.jade all of the results
    });
});

module.exports = router;
