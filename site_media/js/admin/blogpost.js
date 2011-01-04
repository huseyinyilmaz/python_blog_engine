$(function(){
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
	    }
	}
    );

    var BlogPostView = Backbone.View.extend(
	{
	    tagName:"div",
	    className:"mainView",
	    render:function(){
		return this;
	    }
	}
    );

    var blogPost = new BlogPost(data);
    var blogPostView = new BlogPostView({model:blogPost});
    console.log(blogPostView.el)
});
