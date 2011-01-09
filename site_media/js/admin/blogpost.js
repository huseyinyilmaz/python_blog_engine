$(function(){
    //enable logger
    logger.enableLog = true;
    logger.startLog('JQuery initializer');
    //_____________Object that holds dom manipulation functions____________________
    var domManipulator = {
	createRow:function(label,widget){
	    var id = 'id_' + name,
	    tr = $('<tr></tr>').append($('<th></th>')
				       .append($('<label></label>')
					       .attr({for:id})
					       .html(label)
					      )
				      ).append($('<td></td>')
					       .append(widget)
					      );
	    return tr;
	},
	getId:function(name){return 'id_' + name},
	getTextarea:function(name,value,rows,cols){
	    if(!rows)rows="3";
	    if(!cols)cols=""
	    return $('<textarea></textarea>').attr({id:this.getId(name),
						    name:name,
						    rows:rows,
						    cols:cols}).addClass('grid_7').html(value);
	},
	getTextInput:function(name,value){
	    return $('<input></input>').attr({id:this.getId(name),name:name,type:'text'}).addClass('grid_7').val(value);
	},
	getCheckbox:function(name,isChecked){
	    var checkbox= $('<input></input>').attr({id:this.getId(name),
						     name:name,
						     type:'checkbox'}).addClass('grid_7');
	    if(isChecked)
		checkbox.attr({checked:'checked'});
	    return checkbox
	}
    };//domManipulator
    //______________________Jquery UI initialization___________________
    var dialog = $("#messageBox").dialog({ hide: 'blind',
					   autoOpen:false,
					   buttons: { "Ok": function(){ dialog.dialog("close");}}
					 });

    //_______________________Program Logic_____________________________
    var Tag = Backbone.Model.extend();
    var Category = Backbone.Model.extend();
    var Tags = Backbone.Collection.extend({model:Tag});
    var Categories = Backbone.Collection.extend({model:Category});
    var BlogPost = Backbone.Model.extend(
	{
	    initialize:function(){
		logger.startLog('BlogPost.initialize');
		this.tags = new Tags(this.get("tags"));
		this.categories = new Categories(this.get("categories"));
		this.unset("tags",{"silent":true});
		this.unset("categories",{"silent":true});
		this.bind("change",function(model){this.onChanged(model)})
		logger.endLog();
	    },//initialize
	    url:blog_url,
	    onChanged:function(model){
		logger.log("I am here");
		logger.log(model);
		model.save(undefined,{
		    success:function(model,result){
			logger.startLog("save-success-callback");
			logger.log(result)
			logger.endLog();
			window.location = next_url;

		    },
		    error:function(model,xhrObject){
			logger.startLog("save-error-callback");
			logger.log(xhrObject);
			var title = xhrObject.status==0?'Error':'Status : ' + xhrObject.status; 
			var message = xhrObject.status==0?'Could not reach the server' : xhrObject.statusText;
			//show error dialog
			dialog.dialog('option','title',title);
			$("#messageContent",dialog).html(message);
			dialog.dialog("open");
			//make model dirty
			model._changed=true;
			logger.endLog();
		    }
		});
	    }
	}
    );

    var BlogPostView = Backbone.View.extend(
	{
	    tagName:"div",
	    className:"mainView",
	    render:function(){
		logger.startLog('BlogPostView.render')
		var d = $(document.createDocumentFragment()),
		table=$('<table></table>').appendTo(d);
		
		table.append(domManipulator.createRow('Published:',domManipulator.getCheckbox('published',this.model.get('published'))));
		table.append(domManipulator.createRow('Title:',domManipulator.getTextInput('title',this.model.get('title'))));
		table.append(domManipulator.createRow('Slug:',domManipulator.getTextInput('slug',this.model.get('slug'))));
		table.append(domManipulator.createRow('Teaser:',domManipulator.getTextarea('teaser',this.model.get('slug'),5)));
		table.append(domManipulator.createRow('Content:',domManipulator.getTextarea('content',this.model.get('slug'),15)));
		
		$(this.el).append(table);
		logger.endLog();
		return this;
	    },
	    onOKPressed:function(){
		logger.startLog('BlogPostView.onOKPressed');
		function getId(name){
		    return "#" + domManipulator.getId(name);
		}
		data = {
		    "published":$(getId("published")).attr("checked"),
		    "title":$(getId("title")).val(),
		    "slug":$(getId("slug")).val(),
		    "teaser":$(getId("teaser")).val(),
		    "content":$(getId("content")).val()
		       }
		logger.log(data);
		this.model.set(data);
		logger.endLog();
	    },
	    onCancelPressed:function(){
		logger.startLog('BlogPostView.onCancelPresed');
		window.location = next_url;
		logger.endLog();
	    }


	}
    );
    var blogPost = new BlogPost(data);
    logger.log('Blog post was created from json data');
    var blogPostView = new BlogPostView({model:blogPost});
    //connect BlogPostView with dom
    $('#blogPostMainForm').append(blogPostView.render().el);
    //connect buttons
    $('#saveButton').click(function(){blogPostView.onOKPressed();});
    $('#cancelButton').click(function(){blogPostView.onCancelPressed();});
    logger.endLog();
});
