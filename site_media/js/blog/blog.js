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
      var postValueField = $('#postValueField');
      
      submitButton.click(function(){
			     logger.startLog('submitButton.click');
			     var obj = form.serializeObject();
			     var json = JSON.stringify(obj);
			     obj.value = postValueField.val();
			     logger.log(obj);
			     logger.log(json);
			     $.post(comment_form_url, obj,
				    function(data) {
					alert("Data Loaded: " + data);
				    });
			     
			     logger.endLog();
			 });
      logger.endLog();
  });
