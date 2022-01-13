
var http = require('http');
var iconv = require('iconv-lite');
var async = require('async');


// const arrayParam = ["userNo", "url", "videoName", "sessionId", "isRealTime", "level"];

// ************      수정부분     *************** //
const arrayParam = ['id','subj','text']
const arrayParam2 = ['resno','subj','year','subjseq','sulnum','selnum','sulmasid','suldetid','seqno','seltext']


const arrayErrorMsg = ["invalid request", "invalid url", "download failed"];
const arrayParamSize = arrayParam.length;

const pythonScriptPath = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\nsmc-master";
const charSet = 'UTF-8';
                    
//import library
//필요한 모듈 설치해줘야함
var dateFormat = require('dateformat');
var fs = require('fs');
var utf8 = require('utf8');

// node 버전에 따라 호환이 안되서 대체
// var pythonShell = require('python-shell');
let {PythonShell} = require('python-shell');

var request = require("request");
var winston = require('winston');

const logDir = 'log';
var tsFormat;
// --------------------------------------------------------------
//
// Class Variables
//
// --------------------------------------------------------------
var paramMap = new Map();
var url = new String();

var mode = "transcoding";

var now;
var date;
var datetime;
var logger;


function getResultJson(success, msg) {
  logger.info("=========================getResultJson=====================");
  var result = {}; // {}:key,value를 가지는 객체 | []:배열 
  result["success"] = success;
  return result;
}

// test !! Success

// 일단 하나만 받는다고 가정할 것 
// async, await을 쓰려면 promise가 있어야함.. 지금 상태는 작동안할 것 
function lego(){
  console.log('======================lego=====================');
  var pyArgs = [];

    // id, subj, text 를 인자로 넣는다.
    pyArgs.push(paramMap.get(arrayParam[0]));
    pyArgs.push(paramMap.get(arrayParam[1]));
    pyArgs.push(paramMap.get(arrayParam[2]));
  
    console.log('pyArgs[0] : ',pyArgs[0]);
    console.log('pyArgs[1] : ',pyArgs[1]);
    console.log('pyArgs[2] : ',pyArgs[2]);

  var options = {
    mode: 'text',
    pythonPath: '',
    pythonOptions: ['-u'],
    scriptPath: pythonScriptPath,
    args: pyArgs
  };
  
  var finalresult = '';

  console.log("pythonShell.run 들어가기전")
  PythonShell.run('finalAnalyize.py', options, function (err, results) {
    if (err) {
      console.log('python script error!', err);
      throw err;
    }
    
    // finalresult = results[0].slice(2,-2)
    // console.log('results[0].slice(2,-2):', results[0].slice(2,-2));
    // console.log('typeof(results[0].slice(2,-2)) :', typeof(results[0].slice(2,-2)));
    // finalresult = finalresult.split('\', \'')
    // console.log('finalresult : ', finalresult);
    // console.log('typeof(finalresult):', typeof(finalresult));

    console.log('PythonShell results: %j', results);
  });

  // 리스트 ['text값','emotion값','score값'] 리턴 
  return finalresult;

}

module.exports.toJSON = function(res, req, next){

  // req가 json으로 왔으니 그걸 바로 JSON.parse하면된다.
  
  var lion = req.NAME;
  console.log(lion);
  //console.log(req.body);
  // var lion = JSON.parse(req);
  // var arrlength = lion.users.length();
  // for(var i = 0; i < arrlength; i++){
  //   console.log(lion.users[i].seltext);
  // }
  res.send("ok" + lion)

}
