hlan = {};
// debug 开启时在控制台打印日志
hlan.debug=true
hlan.res = {}
hlan.menu = {}
// 自己构建日志打印，方便集中控制
hlan.log=function(s){
	hlan.debug && console.log(s)
}



hlan.app_send = function(retfun,app, method, params) {
	/*
	 
	 */
	p = {};
	if(typeof(method) != "undefined" && method != '') {
		p.method = method;
	} else {
		hlan.log('method error');
		return;
	}
	if(typeof(params) == 'undefined') {
		params = {}
	}
	p.retfun = retfun;
	p.params = JSON.stringify(params);
	p.id = new Date().getTime();
	try {
		$.post('/app/'+app, p, function(data, status) {
			msg = JSON.parse(data)
			hlan.res[msg.id] = msg.retdata
			/*
			 回调函数，所有的和接口交互都可以使用这个。
			 onclick="hlan.app_send('函数名','app名','app模块名','app模块需要的参数')"
			 接受函数需要从浏览器存储取出来数据
			 exp:
			 funcation test(id){
			 	hlan.log(hlan.res[id])
			 }
			 */
			eval(msg.retfun + '("' + msg.id + '")')
		});
	} catch(err) {
		hlan.log('-----ws_send websokect发送报错');
		hlan.log(err);
	}
	return ''

}
var ws;
hlan.websocket = function() {
	ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

	ws.onopen = function() {
		// Web Socket 已连接上，使用 send() 方法发送数据
		hlan.debug && console.log('ws success connect');

	};

	ws.onmessage = function(evt) {
		try {
			var msg = JSON.parse(evt.data);
		} catch(err) {
			console.log('接受的数据格式不正确')
		}
		try {
			id=new Date().getTime();
			hlan.res[id]=msg.retdata
			/*
			 监听函数，用来接受服务端返回的数据
			 服务端利用websocket.send(data)发送
			 接受函数需要从浏览器存储取出来数据
			 exp:
			 funcation test(id){
			 	hlan.log(hlan.res[id])
			 }
			 */
			eval(msg.retfun + '("' + id + '")')
		} catch(err) {
			hlan.log(err)
			hlan.log('执行' + msg.retfun + '失败')
		}

	};

	ws.onclose = function() {
		// 关闭 websocket
        hlan.log('websocket断开链接了')

	};
}
hlan.ws_send = function(retfun, method, params) {
    /*
        exp: hlan.ws_send('print','test.mod1','')
     */
	p = {};
	if(typeof(method) != "undefined" && method != '') {
		p.method = method;
	} else {
		console.log('method error');
		return;
	}
	if(typeof(params) == 'undefined') {
		params = {}
	}
	p.retfun = retfun;
	// p.params = JSON.stringify(params);
    p.params = params;
	p.id = new Date().getTime();
	try {
		ws.send(JSON.stringify(p))
	} catch(err) {
		console.log('-----ws_send websokect发送报错');
		console.log(err);
	}

}
