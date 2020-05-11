<?php
	header("Content-type:text/xml");
	header("Access-Control-*");
	
	//The path can be external. For instance, we can supply
	// "www.bbcnews.com/feeds.xml" as the parameter.
	// This script is now acting as a PROXY server script.
	
	//Two ways of making cross-domain calls from a browser- 
	// a) Use Access-Control-* headers
	// b) Make a call to your own server and make the server call
	//    the external domain. The server is now a PROXY server.
	// In the current example, the server is a PROXY
	$feed = file_get_contents("feeds.xml");
	
	echo $feed;

?>