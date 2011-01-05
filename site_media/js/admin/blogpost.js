$(function(){
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
    
    var Tag = Backbone.Model.extend();
    var Category = Backbone.Model.extend();
    var Tags = Backbone.Collection.extend({model:Tag});
    var Categories = Backbone.Collection.extend({model:Category});
    var BlogPost = Backbone.Model.extend(
	{
	    initialize:function(){
		this.tags = new Tags(this.get("tags"));
		this.categories = new Categories(this.get("categories"));
		this.unset("tags",{"silent":true});
		this.unset("categories",{"silent":true});

	    }//initialize
	}
    );

    var BlogPostView = Backbone.View.extend(
	{
	    tagName:"div",
	    className:"mainView",
	    render:function(){
		var d = $(document.createDocumentFragment()),
		table=$('<table></table>').appendTo(d);
		
		table.append(domManipulator.createRow('Published:',domManipulator.getCheckbox('published',this.model.get('published'))));
		table.append(domManipulator.createRow('Title:',domManipulator.getTextInput('title',this.model.get('title'))));
		table.append(domManipulator.createRow('Slug:',domManipulator.getTextInput('slug',this.model.get('slug'))));
		table.append(domManipulator.createRow('Teaser:',domManipulator.getTextarea('teaser',this.model.get('slug'),5)));
		table.append(domManipulator.createRow('Content:',domManipulator.getTextarea('content',this.model.get('slug'),15)));
		
		$(this.el).append(table);
		return this;
	    }
	}
    );

    var blogPost = new BlogPost(data);
    var blogPostView = new BlogPostView({model:blogPost});

    $('#blogPostMainForm').append(blogPostView.render().el)

});
