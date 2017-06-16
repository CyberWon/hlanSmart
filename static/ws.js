var ws = new WebSocket('ws://'+ document.domain + ':' + location.port +'/ws');
//正式版本只需要注释掉就不会在控制台输出
function print(s)
{
	console.log(s);
}
ws.onopen = function()
{
// Web Socket 已连接上，使用 send() 方法发送数据
	print('ws success connect');

};

ws.onmessage = function (evt) 
{ 
	try
	{
		var msg = JSON.parse(evt.data);
	}
	catch(err)
	{
		print('接受的数据格式不正确')
	}
	try
	{
		eval(msg.retfun+'("'+msg.retdata+'")')
	}
	catch(err)
	{
		print(err)
		print('执行'+msg.retfun+'失败')
	}
	
};

ws.onclose = function()
{ 
// 关闭 websocket

};
function ws_send(method,params){
	p={"jsonrpc":"2.0"};
	if (typeof(method) != "undefined" && method != '') {
		p.method=method;
	}
	else{
		console.log('method error');
		return;
	}
	if (typeof(params)=='undefined'){
		params={}
	}
	p.params=params;
	p.id=new Date().getTime();
	try
	{
		ws.send(JSON.stringify(p))
	}
	catch(err)
	{
		print('-----ws_send websokect发送报错');
		print(err);
	}
	
}
