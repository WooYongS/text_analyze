
// 라우트 메소드는 HTTP 메소드 중 하나로부터 파생되며, 
// express 클래스의 인스턴스에 연결됩니다.

var express = require('express');
var router = express.Router();
var qs = require('querystring');

// /* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express hi!! gogogo!' });
});

var aiText = require('../controllers/aiText');
var aiText_Bak = require('../controllers/aiText_Bak');
var aiText_analysis = require('../controllers/aiText_analysis');


router.post('/aiText_Bak',function(req, res, next){
  aiText_Bak.toJSON(res,req);
});

// pug로 표현해야하는 페이지 
router.get('/inputSubj', function(req, res, next){
  console.log('filename : ' + __filename);
  console.log('dirname : ' + __dirname);
  res.send(`

  <form action="/aiText_Bak" method="POST">
    <p><input type="text" name="subjectNumber" placeholder="subjectNumber"></input></p>
    <p><input type="text" name="year" placeholder="year"></input></p>
    <p><input type="text" name="subjseq" placeholder="subjseq"></input></p>
    <p>
      <input type="submit"></input> 
    </p>
  </form>

  `);
  // res.send("아아아");
});

router.get('/aiText', function(req, res, next){
  //res.render('index', { title: 'Express hi!! gogogo!' });
  aiText.analyize(res,req);
});

router.post('/aiText', function(req, res, next){
  //res.render('index', { title: 'Express hi!! gogogo!' });
  aiText.analyize(res,req);
});

router.post('/aiText_analysis',function(req, res, next){
  // console.log(req) 
   aiText_analysis.toJSON(res,req);
  //console.log("1111");
  //var resJson = {"key":"true"}
  //res.send(resJson);
});

router.get('/Hell', function(req, res, next){
  res.send(`

    <!DOCTYPE html>
    <html lang="ko">

      <head>
      </head>
      <body>
          <div class="row">
            <div class="col-sm-12 col-md-12">
              <div class="box">

                <div class="box-header">
                  <h3>분석정보 셋팅</h3>
                 <small>분석할 정보를 셋팅합니다.</small>
                </div>

              <div class="box-body">
                    <div calss="row">
                        <div class="col-sm-4 col-md-4">

                          <div class="form-group row">
                              <label class="col-sm-3 form-control-label">과정코드</label>
                              <div class="col-sm-9">
                                <input id="subj" type="text" minlength="7" maxlength="7" class="form-control" placeholder="과정코드를 입력하세요(7자리)">
                              </div>
                            </div>

                          <div class="form-group row">
                            <label class="col-sm-3 form-control-label">연도</label>
                            <div class="col-sm-9">
                              <input id="year" type="text" minlength="4" maxlength="4" class="form-control" placeholder="분석 시작 년도">
                            </div>
                          </div>

                          <div class="form-group row">
                            <div class="col-sm-12 text=right">
                              <button id="sul_search" type="button" class="btn info" job="search">조회</button>
                            </div>
                          </div>

                        </div>
                      </div>
                </div>
              </div>
          </div>

            <div class="cole-sm-6 col-md-6">

                <div class=box">
                    <div class="box-header">
                          <h3>분석정보 조회</h3>
                        <small>분석 정보를 확인하세요.</small>
                     </div>
                  
                    <div class="box-body">
                        <div class="row">
                            <div class="col-sm-12 col-md-12">

                              <div class="form-group row">
                                <textarea id="sul_info" class="form-control" rows="15" required placeholder="분석정보 표시 영역" readonly></textarea>
                              </div>

                              <div class="form-group row">
                                <div class="col-sm-12 text-right">
                                  <button id="sul_send" type="button" class="btn info" job="search">분석 시작</button>
                                </div>
                              </div>

                             </div>
                         </div>
                     </div>
                 </div>
              </div>

              <div class="col-sm-6 col-md-6">
                  <div class="box">
                        <div class="box-header">
                            <h3>분석결과 확인</h3>
                          <small>결과를 확인하세요.</small>
                        </div>
                        <div class="box-body">
                            <div class="row">
                                <div class="col-sm-12 col-md-12">

                                <div class="form-group row">
                                  <textarea id="sul_result" class="form-control" rows="15" required placeholder="분석정보 표시 영역">
                                  </textarea>
                                </div>

                              </div>
                           </div>
                     </div>
                 </div>

            </div>
          </div>
          </div>

      //<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
      <script src="http://code.jquery.com/jquery-latest.min.js"></script>

      <script>

          $(document).ready(function(){

            // 조회 버튼
            $("#sul_search").on("click",function(){
              
              var subj = $("#subj").val();
              var year = $("#year").val();
              var job = $(this).attr("job");

                $.ajax({
                  type:"post",
                  url:"http://ehrd.kbstar.com/pr/!kbm_aitxt.saSulData?p_subj="+subj+"&p_year="+year+"&p_job="+job,
                  complete:function(result){

                    var result_txt = result.responseText;
                    result_txt = decodeURIComponent(unescape(result_txt));

                    if(result_txt.indexOf("err") == -1){
                      result_txt = result_txt.substr(0,result_txt.length-6);
                      result_txt = result_txt + "]}";
                      $("#sul_info").val(result_txt); 
                    }else{
                      alert(result_txt.split("_")[1]);
                    }

                  }
                });
              });
            //조회 버튼 끝

            //분석 시작 버튼
            $("#sul_send").on("click",function(){
                  var sul_info = $("#sul_info").val();
                  console.log(sul_info);

                
                // JSON.parse를 하는 순간 string에서 Object(JSON)객체가 되버리는 것임
                // 근데 ajax post json을 보면.. obejct를 보내는 게 아니라 string을 보내는 거임(?)

                //var obj_sul_info = JSON.parse(sul_info);
                $("#sul_result").val(sul_info);
                
                
                // obj_sul_info에 모든 정보는 다 담아왔다.이제 게임 끝 보내자 파이썬으로
                var dataJson = {"name":"ironman"}
                $.ajax({
                    method:"post",
                    url:"/aiText_analysis",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    //data: JSON.stringify(sul_info),
                    //data:{"name":"ironman"},
                    data : dataJson, 
                    success:function(result){
                      // ok, 잘보내진다. 결과값 가져올꺼야? 몰라 일단 신경꺼 보내서 처리해 
                      //var result_txt = result.responseText;
                      //var obj = JSON.parse(result_txt);
                      //$("#sul_result").val(obj.num);
                    },
                    error:function(data){
                      alert("fail");
                    }
                });
                


            })



           });

      </script>

      </body>
    
    </html>

  
  
  `);
});



module.exports = router;

