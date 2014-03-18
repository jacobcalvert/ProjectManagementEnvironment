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
function init_handlers()
{
	$("#login").click(login);
	$("#gnode").click(gnode);
	$("#inode").click(inode);
}
function init()
{
	connect_ws();
	init_handlers();
}
function login()
{
	msg = {"req_type":"login","username":$("#un").val(), "passhash":$("#ph").val()};
	log(JSON.stringify(msg),window.logging.level.INFO,"login");
	window.ws.handle.send(JSON.stringify(msg));
}
function gnode()
{
	msg = {"req_type":"get_node","node_id":$("#gnid").val(),"auth_token":window.session.auth};
	log(JSON.stringify(msg));
	window.ws.handle.send(JSON.stringify(msg));
}
function inode()
{
	msg = {"req_type":"insert_node","node_id":$("#inid").val(),"content":$("#inc").val(),"parent_node":$("#inp").val(),"auth_token":window.session.auth};
	log(JSON.stringify(msg));
	window.ws.handle.send(JSON.stringify(msg));
}
function ws_open(event)
{
	log("WebSocket has been opened: " + event.data);
}	
function ws_msg(event)
{
	msg = JSON.parse(event.data);
	if (msg.reply_type == "login_success")
	{
		window.session.auth = msg.auth_token;
	}
	else if (msg.reply_type == "get_node")
	{
		html = "";
		for (i = 0; i < msg.num_results; i++)
		{
			html += "<div class ='getnode'>";
			html += "<li>"+msg.results[i].id + "</li>";
			html += "<li>"+msg.results[i].parent + "</li>";
			html += "<li>"+msg.results[i].content + "</li>";
			html += "</div>";
			html+= "<hr>";
			
		}
		$("#results").html(html);
	}
	log("Rx'd message ("+event.data+") on WebSocket connection.");
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
