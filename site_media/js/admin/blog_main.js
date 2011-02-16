$(function(){
	  //initilize links
	  $("button.item").click(function(e){
								 window.location = $(this).val();
							 });
      //holds a jquery object
      var selectedRow = null;
      //initialize grid rows
      $("tr.grid_row").click(
          function(){
    	      if(selectedRow != null){
    			  selectedRow.removeClass("ui-state-highlight");
			  }else{
				  $("#grid_button_select").button('option','disabled',false);
				  $("#grid_button_delete").button('option','disabled',false);
			  }
    	      selectedRow = $(this);
    	      selectedRow.addClass("ui-state-highlight");
    	  }//onclick handler
      ).hover(
    	  function(){
    	      if(!selectedRow || selectedRow.get()[0] !== this ){
    			  $(this).addClass("ui-state-hover").removeClass("ui-widget-content");
    	      };
    	  },function(){
    	      $(this).removeClass("ui-state-hover").addClass("ui-widget-content");
    	  });//click
      //initialize buttons
      $("#grid_button_create").button().click(
		  function(){
			  window.location=createUrl;
		  });
      $("#grid_button_select").button({disabled:true}).click(
		  function(){
			  window.location = selectedRow.children("input.selectUrl").val();
		  });
      $("#grid_button_delete").button({disabled:true}).click(
		  function(){
			  $("#deleteDialog").html(delete_message + " '" + selectedRow.children("td:eq(1)").html() + "' ?");
			  $("#deleteDialog").dialog('open');
		  });
      $(".item").button();//list items

      //initialize delete confirmation dialog
      $("#deleteDialog").dialog({resizable: false,
								 height:200,
								 width: 600,
								 modal: true,
								 autoOpen: false,
								 buttons: {
									 'Delete': function() {
										 window.location = selectedRow.children("input.deleteUrl").val();
									 },
									 'Cancel': function() {
										 $(this).dialog('close');
									 }
								 }
								});
  });//onready
