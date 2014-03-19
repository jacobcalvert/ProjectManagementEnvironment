jQuery(document).ready(function(){

// SETUP PARAMS

window.ws = {};
window.ws.base_url = "ws://localhost:8022/ws";
window.ws.handle = null;
window.logging = {};
window.logging.level = {};
window.logging.level["INFO"] = 1;
window.logging.level["WARN"] = 2;
window.logging.level["ERR"] = 3;
window.logging.level["FATAL"] = 4;
window.logging.level["NONE"] = 100;
window.logging.set_level = window.logging.level.INFO;
window.session = {}
window.session.auth = null;


function connect_ws()
{
	window.ws.handle = new WebSocket(window.ws.base_url);
	window.ws.handle.onopen = ws_open;
	window.ws.handle.onmessage = ws_msg;
	window.ws.handle.onclose = ws_close;
	window.ws.handle.onerror = ws_err;
}
function set_handlers()
{
	$(".node").unbind('click');
	$(".node").click(function(event){ window.location.hash = $(this).attr("id");});
	$(window).unbind('hashchange');
	$(window).bind('hashchange',function()
	{
		hash = document.URL.substr(document.URL.indexOf('#')+1) ;
		get_node(hash)
	});
	
}
function init()
{
	connect_ws();
	set_handlers();
}
function login()
{
	msg = {"req_type":"login","username":"jacob", "passhash":"passhash"};
	log(JSON.stringify(msg),window.logging.level.INFO,"login");
	window.ws.handle.send(JSON.stringify(msg));
}
function get_node(id)
{
	msg = {"req_type":"get_node", "auth_token":window.session.auth,"node_id":id}
	msg = JSON.stringify(msg);
	log(msg);
	window.ws.handle.send(msg);
}
function ws_open(event)
{
	log("WebSocket has been opened: " + event.data);
	login();
	setTimeout(function(){
	var hash = document.URL.substr(document.URL.indexOf('#')+1) 
	
	get_node(hash);},1000);
}	
function ws_msg(event)
{
	log("Rx'd message ("+event.data+") on WebSocket connection.");
	msg = JSON.parse(event.data);	
	if (msg.reply_type == "login_success")
	{
		window.session.auth = msg.auth_token;
	}
	else if (msg.reply_type == "get_node")
	{
		html = "";
		if (msg.num_results > 0)
		{
			window.location.hash = msg.results[0].parent;
		}
		else
		{
			alert("No children.");
			history.back();
		}
		for (i = 0; i < msg.num_results; i++)
		{
			html += "<div class ='node' id='"+msg.results[i].id+"'>";
			contents = JSON.parse(msg.results[i].content);
			html += "<h1>" + contents.title + "</h2>";
			html += "<p>" + contents.description + "</p>";
			html += "<p>Date: " + contents.date_created + "</p>";
			html += "</div>";
			
		}
		$("#main").html(html);
		set_handlers();
	}

}
function ws_close(event)
{
	log("WebSocket closed: " + event.data);
}
function ws_err(event)
{
	log("WebSocket error: "+ event.data);
}
function log(event, level, sender)
{
	if (sender == undefined)
	{
		sender = "INFO";
	}
	if (level == undefined)
	{
		level = window.logging.level.INFO;
	}
	if (level >= window.logging.set_level)
	{
		line = sender + " - " + event;
		console.log(line);
	}
	
}


init();
});
