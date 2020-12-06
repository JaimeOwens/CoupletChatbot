//连接配置
var mysql      = require('mysql');
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

//查询用户信息
function userQuery(user_id){
  var userid = user_id;                     //这里的userid会不会串用？
  var sql = "SELECT * FROM User WHERE userid="+userid;
  connection.query(sql,function(err,result){
    if(err){
      return console.log(err.message);
    }
    else{
      var dataString = JSON.stringify(result);//转换为json格式
      var data = JSON.parse(dataString);
      console.log(data);
      var res = data;
    }
  })
  return res;
}
//用户修改信息
function userChange(data){
  var sql = "UPDATE User SET username=?,password=? WHERE userid=?";
  var SqlParams = [data.username,data.password,data.user_id];
  connection.query(sql,SqlParams,function(){
    if(err){
      console.log('insert err',err.message);
      return res=0;
  }
  console.log('insert success');
  });
  return res=1;
}

//用户查询一轮对联记录
var getUsercorpus = function(user_id){
  //查询用户一轮对话的uuid
  var uuidsql="SELECT uuid FROM Corpus WHERE userid="+user_id+"limit 1 orderby desc";
  connection.query(uuidsql, function (err, result){
    if (err) {
      return console.error(err.message);
    }
    else{
      var uuid = result;
    }
  });
  //根据userid
  var sql="SELECT * FROM Corpus WHERE userid="+user_id+" uuid="+uuid;
  connection.query(sql,function(err,res){
    if(err){
      return console.error(err.message);
    }
    else{
      var dataString = JSON.stringify(res);//转换为json格式
      var data = JSON.parse(dataString);
      console.log(data);
      var Usercorpus = data;
    }
  })
  return Usercorpus;
}

//用户修改对联记录
var saveUsercorpus = function(data){
  var saveSql='UPDATE Corpus SET first_couplet = ?,second_couplet = ?,status=False WHERE uuid=? AND userid=? AND timestamp = ?';
  var SqlParams = [data.first_couplet,data.second_couplet,status,uuid,user_id,data.timestamp];
  connection.query(saveSql,SqlParams,function(err){
    if(err){
      console.log('insert err',err.message);
      return;
  }
  console.log('insert success');
  });
  return res='success';
}

//用户查询所有对联记录
function getAllcorpus(user_id){
  var sql="SELECT * FROM Corpus WHERE userid="+user_id;
  connection.query(sql, function (err, result){
    if (err) {
      return console.error(err.message);
    }
    else{
      var dataString = JSON.stringify(result);//转换为json格式
      var data = JSON.parse(dataString);
      console.log(data);
      var Allusercorpus = data;
    }
  });
  return Allusercorpus;
}


