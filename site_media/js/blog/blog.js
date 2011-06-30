//http://stackoverflow.com/questions/1184624/serialize-form-to-json-with-jquery
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(function(){
      logger.startLog("onLoad");
      var form = $('#commentForm');
      var submitButton = $('#commentSubmit');
      var formContainer = $('#formContainer');
      var highlightDiv = $('#highlightDiv');
      var highlightTitle = $('#highlightTitle');
      var highlightMessage = $('#highlightMessage');
      highlightDiv.hide();
      //initilize buttons
      submitButton.button().click(function(){
				      logger.startLog('submitButton.click');
				      var obj = form.serializeObject();
				      logger.log(obj);
				      $.post(comment_form_url, obj,
					     function(data) {
						 logger.startLog("submit button callback");
						 if(data.success){
						     logger.log("Comment successfully completed");
						     highlightDiv.slideDown("fast");
						 }else{
						     logger.log("Comment have an error");
						     formContainer.html("<table>" + data.form + "</table>");
						 };
						 logger.endLog();
					     },'json');
			     
				      logger.endLog();
				  });
      logger.endLog();
  });
