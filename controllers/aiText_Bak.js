var http = require('http');
var iconv = require('iconv-lite');
var async = require('async');

var config = require('../config/config.js');
var PImage = require('pureimage')

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

const arrayParam = ['subj','year','subjseq'];
const arrayParam2 = ['cnt','resno','subj','year','subjseq','sulnum','selnum','sulmasid','suldetid','seqno','seltext']

const arrayErrorMsg = ["invalid request", "invalid url", "download failed"];
const arrayParamSize = arrayParam.length;

const pythonScriptPath = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\nsmc-master";
const charSet = 'UTF-8';
                    
// hrd2 서버의 이미지업로드 모듈 경로
const imgUploadUrl = config.imgUploadUrl;

// 워드클라우드 이미지 생성시 저장할 위치 '키':'값' 매칭
uploadFiles = {};
uploadFiles['file1'] = 'C:\\Users\\User\\Desktop\\work\\nodejs_workplace\\endGame\\bin\\1211517_2020_0002_wordcloud.png'

console.log('======================>'+uploadFiles['file1']);

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
    // arrayParam >> subj, year, subjseq
    for(var i = 0; i < arrayParam.length; i++){
      pyArgs.push(paramMap.get(arrayParam[i]));
    }
    for(var i = 0; i < arrayParam.length; i++){
      console.log('pyArgs[',i,']: ', pyArgs[i]);
    }
  var options = {
    mode: 'text',
    pythonPath: '',
    pythonOptions: ['-u'],
    scriptPath: pythonScriptPath,
    args: pyArgs
  };
  
  var finalresult = '완료';

  console.log("pythonShell.run 들어가기전")
  PythonShell.run('gotoFINAL.py', options, function (err, results) {
    if (err) {
      console.log('python script error!', err);
      throw err;
    }
    console.log('PythonShell results: %j', results);
  });

  // 리스트 ['text값','emotion값','score값'] 리턴 
  return finalresult;

}

function imageUpload(imgUploadUrl, uploadFiles){

  console.log("----------------------imageUpload--------------------------");
  console.log(imgUploadUrl);
  console.log(JSON.stringify(uploadFiles));

  const form = request.post({
    url:imgUploadUrl,
    header: {
      'Content-Type': 'multipart/form-data'
    }

  }, (error, response, body) => { 

    // 요청 완료 
    if (error) {
      console.log(error);
      console.log(imgUploadUrl);
      //printErrLog(JSON.stringify(uploadFiles));
      //printErrLog(JSON.stringify(uploadValues));
      //printErrLog("error: " + error);
    }
    else{

      console.log("response.statusCode: " + response.statusCode);
      console.log("=======body start=======")
      console.log("body: " + body); 
      console.log("=======body end=======")
      
      var isError = false;
      if(response.statusCode == 200){
        //response의 result값이 false 일때, 재시도(3회) 
        //var resJson = JSON.parse(body);
        // if(response.statusCode == 200 && resJson.result =="false"){
        //   isError = true;
        // }
        console.log("response.status Code == 200"); 
      }
      else{
        isError = true;
      }
      if(isError){
        console.log("500 Error, 5초 후 재시도(3회)");
      }
    }
  }).form() 

  //데이터를 지정합니다. 
  // form.append(key, value) -> value는 경로명이 들어가있음.
  // 즉, 키값으로 경로를 가져올 거임. 물론 그 경로를 fs화해서 보낸다.

  for(var key in uploadFiles){
   form.append(key, fs.createReadStream(uploadFiles[key]));
  }
  
}


module.exports.toJSON = function(res, req, next){
 
  var subj = req.body.subjectNumber;
  var year = req.body.year;
  var subjseq = req.body.subjseq;

  console.log("subj : "+ subj);
  console.log("year : "+ year);
  console.log("subjseq : "+ subjseq);

  paramMap.set(arrayParam[0], subj);
  paramMap.set(arrayParam[1], year);
  paramMap.set(arrayParam[2], subjseq);

  /////////////////////////
  // 0218 주석 시작

  var pathstring = '/pls/cyber/!kbm_aitxt.saSulData?p_subj=';
  pathstring = pathstring.concat(subj);
  pathstring = pathstring.concat('&p_year=')
  pathstring = pathstring.concat(year);
  pathstring = pathstring.concat('&p_subjseq=')
  pathstring = pathstring.concat(subjseq);
  pathstring = pathstring.concat('&p_job=search')
  console.log('pathstring :', pathstring);

  // var pathstring = '/pls/cyber/z_wootest.test_text?p_subj=1211517&p_num=2'
  // console.log(pathstring);
  
  // 해당 프로시저 서버에서 과목번호에따른 데이터셋을 가져오자.

  var options = {
    host: 'ehrd.kbstar.com',
    path: pathstring
  };

  var fbResponse;

  console.log('http.get:...호출 전');

  http.get(options, function(res){
    var body = '';

    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));

    //결코 순서대로 찍히지 않는다 왜? 비동기임. 요청하고 지나감.
    res.on('data',function(chunk){
      body += chunk;
    });

    res.on('end', function(){
      // JSON의 리스트를 받았다. 리스트의 길이를 구하고
      // 길이만큼 포문을 돌리되 가져올 것만 돌린다. '
      console.log('---------------------res body------------------');

      // sql에서 받은 escape..처리 
      console.log(decodeURIComponent(unescape(body)));
      body = decodeURIComponent(unescape(body));
    });
  }).on('error', function(e){
      console.log("Got an error : ", e);
  });

  console.log('filename : ' + __filename);
  console.log('dirname : ' + __dirname);

  //console.log("============body 출력 끝================")
  //console.log("imageUpload 호출후");
    
  lego();

  //imageUpload(imgUploadUrl,uploadFiles);

  // 0218 주석 끝




}
