var express = require('express');
var router = express.Router();
var request = require("request");

router.get ('/', function (req, res, next) {

    var options = { method: 'GET',
        url: 'https://jobs.github.com/positions.json',
        qs:{ 
            search: req.query.searchterm,
            page: '1',
        headers:
        { 'postman-token': 'ea90e0ac-7c80-e2a4-ab57-3025cc142381',
			'cache-control': 'no-cache' }  } };

    request(options, function (error, response, body) {
        if (error) throw new Error(error);

        //console.log(body);

        var searchterm = req.query.searchterm;
		//console.log(req);
        //res.send({searchterm: searchterm, body: body});
		
		var json_body = JSON.parse(body)
		var titles = []
		for (var i = 0; i < json_body.length; i++){
			var curr_title = json_body[i].title;
			titles.push(curr_title);
			console.log(curr_title);
		}
		
		//res.send(titles);
		res.render('jobs', { jobs: titles });
    });
});

module.exports = router;
