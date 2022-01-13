function uploadEncodedFiles(cloudUploadUrl, uploadFiles){

    logger.info("------------------------uploadEncodedFiles--------------------------");
    logger.info(cloudUploadUrl);
    logger.info(JSON.stringify(uploadFiles));
    logger.info(JSON.stringify(uploadValues)); 
  
    const form = request.post({
      url:cloudUploadUrl,
      header: {
        'Content-Type': 'multipart/form-data'
      }
  
    }, (error, response, body) => { 

      // 요청 완료 
      if (error) {
        printErrLog(cloudUploadUrl);
        printErrLog(JSON.stringify(uploadFiles));
        printErrLog(JSON.stringify(uploadValues));
        printErrLog("error: " + error);
      }
      else{
  
        logger.info("response.statusCode: " + response.statusCode);
        logger.info("body: " + body); 
        var isError = false;
        if(response.statusCode == 200){
          //response의 result값이 false 일때, 재시도(3회) 
          var resJson = JSON.parse(body);
          if(response.statusCode == 200 && resJson.result =="false"){
            isError = true;
          } 
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