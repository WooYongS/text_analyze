

// const arrayParam = ["userNo", "url", "videoName", "sessionId", "isRealTime", "level"];

// ************      수정부분     *************** //
const arrayParam = ['subj','text']
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
// --------------------------------------------------------------
//
//	initialize
//
// --------------------------------------------------------------

// --------------------------------------------------------------
//
// Functions
//
// --------------------------------------------------------------
function getResultJson(success, msg) {
  logger.info("=========================getResultJson=====================");
  var result = {}; // {}:key,value를 가지는 객체 | []:배열 
  result["success"] = success;
  return result;
}

// test !! Success

// module.exports.recon = function (res, req, next) {
//    console.log(req);
//    res.send("ok");
// }

// 일단 하나만 받는다고 가정할 것 
function lego(subj, text){
  logger.info("======================lego=====================");
  console.log('======================lego=====================');

  var pyArgs = [];

  // var subj = paramMap.get(arrayParam[0]);
    pyArgs.push(subj);
    console.log('pyArgs[0] : ',pyArgs[0]);
  // var text = paramMap.get(arrayParam[1]);
    pyArgs.push(text);
    console.log('pyArgs[1] : ',pyArgs[1]);
  
  var options = {
    mode: 'text',
    pythonPath: '',
    pythonOptions: ['-u'],
    scriptPath: pythonScriptPath,
    args: pyArgs
  };
  
  console.log("pythonShell.run 들어가기전")
  PythonShell.run('finalAnalyize.py', options, function (err, results) {
    if (err) {
      //logger.info("python script error!" + err);
      console.log('python script error!', err);
      throw err;
    }

    //logger.info('PythonShell results: %j', results);
    console.log('PythonShell results: %j', results);
  });
}

// MODULE
module.exports.analyize = function (res, req, next) {
  tsFormat = () => (new Date()).toLocaleTimeString();
  logger = winston.createLogger({
    transports: [
      new (winston.transports.Console)({
       timestamp: tsFormat,
       colorize: true,
       level: 'info'
     }),
      new (require('winston-daily-rotate-file'))({
        filename: `${logDir}/%DATE%_aitext.log`,
        timestamp: tsFormat,
        datePattern: 'YYYY-MM-DD'
      })
    ]
  } );

   //파라메터 검증 
  logger.info('\n');
  logger.info('=-=-=-=-=-=-=-= uploadVideo script start =-=-=-=-=-=-=-=');
  console.log('파라미터검증');
  logger.info('\n');
  logger.info(req.body); // req.body로 값들을 다 받아옴...
  for (p in arrayParam) { // arrayParam에 있는 키값들을 순회하면서 원하는 값들을 키에
    // if (!req.body[arrayParam[p]]) {
    //   //optional param
    //   if(arrayParam[p] != 'text'){
    //     res.json(getResultJson(0, 0));
    //     return;
    //   }
    // }
    // 위 배열에 있는 '키'에 따른 '값'이 무엇인지 찍어보기
    logger.info(arrayParam[p] + ' : ' + req.body[arrayParam[p]]);
    console.log(arrayParam[p], ' : ', req.body[arrayParam[p]]);

    // 이제 '키'와'값'을 매칭하여 셋팅
    paramMap.set(arrayParam[p], req.body[arrayParam[p]]);
  }

  // 셋팅해놓은대로..이제 get으로 꺼내와서 원하는 '키'에 값 배정하기   
  subj = paramMap.get(arrayParam[0]);
  text = paramMap.get(arrayParam[1]);

  console.log('다시한번'+subj);
  console.log('다시한번'+text);
  
  lego(subj, text);

  // downloadVideoFile(res);
  res.json(getResultJson(1));
}