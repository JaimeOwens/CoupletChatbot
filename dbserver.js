var express = require('express');
var app = express();
var mysql = require('mysql');
var path = require('path');
var bodyParser = require('body-parser');
const  cors = require('cors')
const contentDisposition = require('content-disposition');
const { url } = require('inspector');
//连接配置

app.use(cors())
var connection = mysql.createConnection({
  host     : '139.9.113.51',
  user     : 'chatbot',
  password : 'chatbot',
  database : 'chatbot'
});
connection.connect((err) => {
  if (err) { console.log("mysql连接失败") }
  else { console.log("mqsql连接成功") }
})
app.use(express.static(path.join(__dirname, 'public')))
//路由设置
app.get('/Index.html',function(req,res){
  res.sendFile(__dirname + "/public/static/"+"Index.html")
})
app.get('/person.html',function(req,res){
  res.sendFile(__dirname + "/public/static/"+"person.html")
})
app.get('/change.html',function(req,res){
  res.sendFile(__dirname + "/public/static/"+"change.html")
})

//查询用户信息
var urlencodedParser = bodyParser.urlencoded({ extended: false })
app.post('/person.html/userQuery',urlencodedParser,function (req,res){
  var userid = req.body.user_id;
  console.log("userid is "+userid);//测试
  var sql = 'SELECT * FROM coupletchatbot_user WHERE userid='+userid;
  connection.query(sql,function(err,result){
    if(err){
      return console.log(err.message);
    }
    else{
      res.json(result);
      // console.log(result);
    }
  })
})
//用户修改信息
app.post('/person.html/userChange',urlencodedParser,function (req,res){
  var sql = "UPDATE coupletchatbot_user SET username=?,password=? WHERE userid=?";
  var SqlParams = [req.body.username,req.body.password,req.body.user_id];
  connection.query(sql,SqlParams,function(err){
    if(err){
      console.log('update err',err.message);
      var msg = 0;
      res.json(msg);
    }
    else{
      console.log('update success');
      var msg = 1;
      res.json(msg);
    }
  });
})

//用户更新并查询一轮对联记录
app.post('/change.html/getUsercorpus',urlencodedParser,function(req,res){
  var Sql='UPDATE coupletchatbot_corpus SET status=?,quality=?,timestamp=? WHERE userid=? AND uuid=?';
  var SqlParams = [0, 0, req.body.timestamp, req.body.user_id, req.body.uuid];
  console.log(SqlParams);
  connection.query(Sql,SqlParams,function(err){
    if(err){
      console.log('update err',err.message);
    }
  })
  
  var sql="select * from coupletchatbot_corpus where uuid=(select uuid from coupletchatbot_corpus where userid= ? order by id desc limit 1)";
  connection.query(sql,req.body.user_id,function(err,result){
    if(err){
      return console.error(err.message);
    }
    else{
      res.json(result);
      // console.log(result);
    }
  })
})

//用户修改对联记录
app.post('/change.html/saveUsercorpus',urlencodedParser,function(req,res){
  var saveSql='UPDATE coupletchatbot_corpus SET first_couplet = ?,second_couplet = ?,status = ? ,quality = ?,timestamp = ? WHERE userid=? AND uuid = ? AND id = ?';
  var SqlParams = [req.body.first_couplet,req.body.second_couplet,req.body.status,req.body.quality,req.body.timestamp,req.body.user_id,req.body.uuid,req.body.id];
  console.log(SqlParams);
  connection.query(saveSql,SqlParams,function(err){
    if(err){
      console.log('update err',err.message);
  }
    else{
      console.log('update success');
      res.send("success");
    }
  });
})

//用户查询所有对联记录
app.post('/person.html/getAllcorpus',urlencodedParser,function(req,res){
  console.log("here are me");
  var userid = req.body.user_id;
  console.log(userid);
  var sql='SELECT * FROM coupletchatbot_corpus WHERE userid = '+userid;
  connection.query(sql,function (err, result){
    if (err) {
      return console.error(err.message);
    }
    else{
      res.json(result);
      // console.log(result);
    }
  });
})

var server=app.listen(7744,function () {
  console.log("loaclhost:7744");
})

