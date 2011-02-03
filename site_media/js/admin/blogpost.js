/*global $, logger, _, Backbone, blog_url, window, next_url, data, URLify, scopeleaks*/
$(function () {
      //enable logger
      logger.enableLog = true;
      logger.showTiming = true;
	  
      logger.startLog('JQuery initializer');

      //______________________Jquery UI initialization___________________
      var dialog = $("#messageBox").dialog({
											   hide: 'blind',
											   autoOpen: false,
											   buttons: {
												   "Ok": function () {
													   dialog.dialog("close");
												   }
											   }
										   });
      var okButton = $("#okButton").button();
      var cancelButton = $("#cancelButton").button();
	  
      //_____________Object that holds dom manipulation functions____________________
      var domManipulator = {
          errorRow: _.template($('#template_error_row').html()),
          row: _.template($('#template_row').html()),
          side_widget: _.template($('#template_side_widget').html()),
          textarea: _.template('<textarea id="<%=id%>" rows="<%=rows%>" cols="<%=cols%>" name="<%=name%>" class="grid_7"><%=content%></textarea>'),
          text_input: _.template('<input type="text" id="<%= id %>" name="<%= name %>" autocomplete="off" class="grid_7" value="<%= content %>"></input>'),
          checkbox: _.template('<input type="checkbox" id="<%= id %>" name="<%= name %> <% if(isChecked){%>checked="checked"<%}%>"'),
          createErrorRow: function (name) {
              var error_id = this.getErrorId(name),
              tr = $(this.errorRow({
									   id: error_id
								   }));
              $('#' + error_id, tr).hide();
              return tr;
          },
		  
          createRow: function (label, name, widgetStr) {
              var id = this.getId(name);
              return $(this.row({
									id: id,
									label: label,
									widget: widgetStr
								}));
          },
		  
          getId: function (name) {
              return 'id_' + name;
          },
          getErrorId: function (name) {
              return 'id_error_' + name;
          },
		  
          getTextarea: function (name, value, rows, cols) {
			  rows = rows | "3";
			  cols = cols | "";
              return this.textarea({
									   id: this.getId(name),
									   name: name,
									   rows: rows,
									   cols: cols,
									   content: value
								   });
          },
		  
          getTextInput: function (name, value) {
              return this.text_input({
										 id: this.getId(name),
										 name: name,
										 content: value
									 });
          },
          getCheckbox: function (name, isChecked) {
              return this.checkbox({
									   id: this.getId(name),
									   name: name,
									   isChecked: isChecked
								   });
          },
          disableButtons: function (isDisable) {
              okButton.button('option', 'disabled', isDisable);
              cancelButton.button('option', 'disabled', isDisable);
          }
		  
      }; //domManipulator
      
      //________________main error panel initilization__________________
      var highlightDiv = $("#highlightDiv");
      highlightDiv.hide();
      
      function showError(title, message) {
          $("#highlightTitle", highlightDiv).html(title).next('span').html(message);
          highlightDiv.slideDown('fast');
      }
      
      function hideError() {
          highlightDiv.slideUp('fast');
      }
      
      function showFieldError(fieldName, title, message) {
          var div = $("#" + domManipulator.getErrorId(fieldName) + "_title");
          div.html(title).next('span').html(message);
          $('#' + domManipulator.getErrorId(fieldName)).show();
      }
      
      function hideFieldError(fieldName) {
          $('#' + domManipulator.getErrorId(fieldName)).hide();
      }
      
      //_______________________Program Logic_____________________________
      var WidgetModel = Backbone.Model.extend({
												  //url:tag_url, set ini initialization
												  initialize: function () {
													  logger.startLog("WidgetModel.initialize");
													  logger.log("widget model values:", this.attributes);
													  logger.endLog();
												  },
												  toggle: function () {
													  logger.startLog("widget.toggle");
													  this.set({
																   'selected': !this.get('selected')
															   });
													  logger.log("widget values:", this.attributes);
													  logger.endLog();
												  }
											  });

      var WidgetCollection = Backbone.Collection.extend({
															//url : get in initialization
															//model_url:get in initialization
															model: WidgetModel,
															comperator: function (model) {
																model.get("name").toLowerCase();
															},
															initialize: function (models,options) {
																logger.startLog('WidgetCollection.initialize');
																// set url of collection
																this.url = options.url;
																delete options.url;
																//bind events-----------------------------------
																//bind add event
																this.bind('add',function(item){
																			  logger.startLog("WidgetCollection>add event handler");
																			  item.save(null,{
																							success:function(model,xhr,options){
																								logger.startLog("WidgetCollection>add>save>success");
																								logger.log('item was successfully saved',model,xhr,options);
																								//If there is a validation errror make sure that they are coming as 404 or 500 errors
																								//If is is success we have to send back the model object with new id and render widget from beginning
																								model.collection.view.render();
																								logger.endLog();
																							},
																							error:function(model,xhr,options){
																								logger.startLog("WidgetCollection>add>save>error");
																								logger.warn('There was an error during save process',model,xhr,options);
																								model.collection.view.showCreateForm(null,xhr.responseText,model.get("name"));
																								//There was an error on server. remove new model from collection
																								model.collection.remove(model,{silent:true});
																								logger.endLog();

																							}
																						});
																			  logger.endLog();
																		  });
																//bind remove event ---------------------------------
																this.bind('remove',function(model,collection,options){
																			  logger.startLog("WidgetCollection>remove event handler");
																			  model.destroy({
																							 success:function(model,xhr,options){},
																							 error:function(model,xhr,options){}
																						 });
																			  logger.endLog();
																		  });
																
																logger.endLog();
															}
															
														});
      var Widget = Backbone.View.extend({
											//el : $()get in initialization
											//title:get in initialization
											//list : get in initialization
											template: _.template($('#template_side_widget').html()),
											list_template: _.template($('#template_widget_list').html()),
											add_template:_.template($('#template_widget_add').html()),
											events: {
												'change .widget_item': 'itemClicked',
												'click .create_link': 'showCreateForm',
												'click .create_cancel': 'render',
												'click .create_ok': 'createItem',
												'click .edit_button': 'editItem',
												'click .delete_button': 'deleteItem'
											},
											
											initialize: function (options) {
												logger.startLog('WidgetView.initialize(' + options.title + ')');
												//connect widget view to collection
												this.collection.view = this;
												//render main widget elements. and add it to el
												this.el.html(domManipulator.side_widget({title: options.title}));
												//set el to inner element part so we can only rerender that part
												this.el = $('.element-list',this.el);
												this.title = options.title;
												delete options.title;
												this.render();
												//delete message
												var widget = this;
												this.deleteDialog = $('#messageBox-'+this.title.toLowerCase()).dialog({   hide: 'blind',
																														  autoOpen: false,
																														  title: 'Delete Item Dialog'});

												logger.endLog();

											},
											render: function () {
												logger.startLog('WidgetView.render(' + this.title +')');
												logger.log('Render elements',this.collection.toJSON());
												var list_html = this.list_template({list:this.collection.toJSON(),
																					title:this.title.toLowerCase()});
												this.el.html(list_html);
												logger.endLog();
											},

											itemClicked:function(event){
												logger.startLog('WidgetView.itemClicked(' + this.title + ')');
												var item = $(event.target);
												var model = this.collection.get(item.val());
												var is_item_checked = new Boolean(item.attr('checked'));
												console.log('item',item);
												console.log('is_item_checked',is_item_checked);
												model.set({selected:is_item_checked},{silent:true});
												logger.endLog();
											},
											showCreateForm:function(event,error,value){
												logger.startLog('WidgetView.showCreateForm(' + this.title + ')');
												var add_html = this.add_template({error : error,
																				  value : value});
												$('.new_item_container',this.el).html(add_html);
												logger.endLog();
											},
											createItem:function(event){
												logger.startLog('WidgetView.createItem(' + this.title + ')');
												logger.log(event);
												var error = null;
												var input = $('.widget_input',this.el);
												var value = input.val();
												if(this.collection.detect(function(item){
																		 return item.get('name') == value;
																	 })){
													error = "Duplicated value";
												}

												if(!value){
													error = "Name cannot be empty";
												}
												if(error){
													//There was an error. Print error message
													this.showCreateForm(event,error,value);
												}else{
													//There is no error. Create Value
													input.val("");
													this.collection.add({name : value});
												}
												
												logger.endLog();
											},

											deleteItem:function(event){
												logger.startLog('WidgetView.deleteItem(' + this.title + ')');
												var html_id = $(event.target).attr('id').split(':');
												var id = _(html_id).last();
												var model = this.collection.get(id);
												logger.log('Delete item',model);
												var deleteModel = function(){
													model.collection.remove(model);
													$(this).dialog("close");
												};

												this.deleteDialog.dialog( "option", "buttons", { "Yes": deleteModel,
																								 "No": function(){
																									 $(this).dialog("close");
																								 }
																							   });
												$('#messageContent-'+this.title.toLowerCase()).html("Are you sure you want to delete '"+model.get('name')+"'");
												this.deleteDialog.dialog('open');
												//todo fill delete dialog with text
												logger.endLog();
											},
											editItem:function(event){
												logger.startLog('WidgetView.editItem(' + this.title + ')');
												var html_id = $(event.target).attr('id').split(':');
												var id = _(html_id).last();
												var model = this.collection.get(id);
												logger.log('Edit item',model);
												//Change item with text field and let user set its value
												//on enter event save model
												logger.endLog();
											}
											
										});
      
      
      var Category = Backbone.Model.extend();
      var Categories = Backbone.Collection.extend({
													  model: Category
												  });
      
      var BlogPost = Backbone.Model.extend({
											   url: blog_url,
											   initialize: function () {
												   logger.startLog('BlogPost.initialize');
												   var tagCollection = new WidgetCollection(this.get("tags"), {url:tag_url} );
												   
												   this.tags = new Widget({ collection : tagCollection,
																			el: $('#tag_widget'),
																			title:'Tags'
																		  });

												   this.categories = new Categories(this.get("categories"));
												   this.unset("tags", {
																  "silent": true
															  });
												   this.unset("categories", {
																  "silent": true
															  });
												   this.bind("change", function (model) {
																 this.onChanged(model);
															 });
												   this.bind('error', function (model, error, options) {
																 this.errorHandler(model, error, options);
															 });
												   
												   logger.endLog();
											   },
											   //initialize
											   savedata: function () {
												   logger.startLog("BlogPost.savedata");
												   
												   this.save({}, {
																 success: function (model, result) {
																	 logger.startLog("save-success-callback");
																	 logger.log(result);
																	 logger.log(model);
																	 domManipulator.disableButtons(false);
																	 if (result.result === 'ok'){ 
																		 window.location = next_url;
																	 } else if (result.result === 'error') {
																		 showError(result.errorTitle, result.error);
																		 if (result.hasOwnProperty('slug_error')){
																			 showFieldError('slug', '', result.slug_error);
																		 }
																	 }
																	 logger.endLog();
p																	 
																 },
																 error: function (model, xhrObject) {
																	 domManipulator.disableButtons(false);
																	 logger.startLog("save-error-callback");
																	 logger.log(xhrObject);
																	 var title = xhrObject.status === 0 ? 'Error' : 'Status : ' + xhrObject.status;
																	 var message = xhrObject.status === 0 ? 'Could not reach the server' : xhrObject.statusText;
																	 //show error
																	 showError(title, message);
																	 //make model dirty
																	 model._changed = true;
																	 logger.endLog();
																 },
																 silent: true //so save does not trigger onchange event
															 });
												   
											   },
											   onChanged: function (model) {
												   logger.startLog("BlogPost.onChanged");
												   logger.log(model);
												   logger.endLog();
											   },
											   //onchanged
											   validate: function (attrs) {
												   logger.startLog("BlogPost.validate");
												   
												   var errors = {},
												   hasErrors = false;
												   //old is valid value
												   var isValid = this.validator.isValid();
												   
												   var validateField = function (name, visual) {
													   if (attrs[name] === "") {
														   //new field value is empty string
														   errors[name] = visual + " cannot be empty";
														   hasErrors = true;
														   this.validator[name] = false;
													   } else if (attrs[name] !== undefined && !this.validator[name]) {
														   //value has changed and it is not an empty string
														   //and old value was invalid
														   hideFieldError(name);
														   this.validator[name] = true;
													   }
													   
												   };
												   validateField = _.bind(validateField, this);
												   
												   validateField('title', 'Title');
												   validateField('slug', 'Slug');
												   if (attrs.slug && !errors.slug && !this.slugRegEx.test(attrs.slug)) {
													   errors.slug = "Slug value must only contain alfa-numeric values, underscores or hypens";
													   hasErrors = true;
													   this.validator.slug = false;
												   }
												   validateField('content', 'content');
												   
												   //current isValid value is true but old one was false
												   if (!isValid && this.validator.isValid()) {
													   hideError();
												   }
												   logger.endLog();
												   return hasErrors?errors:undefined;
											   },
											   
											   errorHandler: function (model, error, options) {
												   logger.startLog("BlogPost.errorHandler");
												   
												   showError('Validation Error:', 'Please fix following errors.');
												   
												   var fieldError = function (name) {
													   if (error[name]) {
														   showFieldError(name, '', error[name]);
													   }
												   };
												   fieldError('title');
												   fieldError('slug');
												   fieldError('teaser');
												   fieldError('content');
												   fieldError('published');
												   
												   
												   logger.endLog();
											   },
											   
											   validator: {
												   title: true,
												   slug: true,
												   teaser: true,
												   content: true,
												   published: true,
												   isValid: function () {
													   return this.title && this.slug && this.teaser && this.content && this.published;
												   }
											   },
											   slugRegEx: new RegExp("^[a-zA-Z-_0-9]+$")
										   });
      
      var BlogPostView = Backbone.View.extend({
												  tagName: "div",
												  className: "mainView",
												  render: function () {
													  logger.startLog('BlogPostView.render');
													  var table = $('<table></table>');
													  
													  table.append(domManipulator.createErrorRow('published'));
													  table.append(domManipulator.createRow('Published:', 'published', domManipulator.getCheckbox('published', this.model.get('published'))));
													  table.append(domManipulator.createErrorRow('title'));
													  table.append(domManipulator.createRow('Title:', 'title', domManipulator.getTextInput('title', this.model.get('title'))));
													  table.append(domManipulator.createErrorRow('slug'));
													  table.append(domManipulator.createRow('Slug:', 'slug', domManipulator.getTextInput('slug', this.model.get('slug'))));
													  table.append(domManipulator.createErrorRow('teaser'));
													  table.append(domManipulator.createRow('Teaser:', 'teaser', domManipulator.getTextarea('teaser', this.model.get('teaser'), 5)));
													  table.append(domManipulator.createErrorRow('content'));
													  table.append(domManipulator.createRow('Content:', 'content', domManipulator.getTextarea('content', this.model.get('content'), 15)));
													  
													  $(this.el).append(table);
													  logger.endLog();
													  return this;
												  },
												  onOKPressed: function () {
													  logger.startLog('BlogPostView.onOKPressed');
													  domManipulator.disableButtons(true);
													  var getId = function (name) {
														  return "#" + domManipulator.getId(name);
													  };
													  var data = {
														  "published": $(getId("published")).attr("checked"),
														  "title": $(getId("title")).val(),
														  "slug": $(getId("slug")).val(),
														  "teaser": $(getId("teaser")).val(),
														  "content": $(getId("content")).val()
													  };
													  logger.log(data);
													  this.model.set(data);
													  this.model.savedata();
													  logger.endLog();
												  },
												  onCancelPressed: function () {
													  logger.startLog('BlogPostView.onCancelPresed');
													  window.location = next_url;
													  logger.endLog();
												  },
												  events: (function () {
															   var e = {};
															   e['change #' + domManipulator.getId('title')] = 'onTitleChanged';
															   e['change #' + domManipulator.getId('slug')] = 'onSlugChanged';
															   e['change #' + domManipulator.getId('teaser')] = 'onTeaserChanged';
															   e['change #' + domManipulator.getId('content')] = 'onContentChanged';
															   e['change #' + domManipulator.getId('published')] = 'onPublishedChanged';
															   
															   return e;
														   }()),
												  onChangeField: function (event, name) {
													  logger.startLog('blogPostView.onTitleChanged');
													  this.model.set((function () {
																		  var obj = {};
																		  obj[name] = event.target.value;
																		  logger.log(obj);
																		  return obj;
																	  }()));
													  logger.endLog();
												  },
												  onTitleChanged: function (event) {
													  logger.startLog('blogPostView.onTitleChanged');
													  this.onChangeField(event, 'title');
													  logger.endLog();
												  },
												  
												  onSlugChanged: function (event) {
													  logger.startLog('blogPostView.onSlugChanged');
													  this.onChangeField(event, 'slug');
													  logger.endLog();
												  },
												  onTeaserChanged: function (event) {
													  logger.startLog('blogPostView.onTeaserChanged');
													  this.onChangeField(event, 'teaser');
													  logger.endLog();
												  },
												  onContentChanged: function (event) {
													  logger.startLog('blogPostView.onContentChanged');
													  this.onChangeField(event, 'content');
													  logger.endLog();
												  },
												  onPublishedChanged: function (event) {
													  logger.startLog('blogPostView.onPublishedChanged');
													  this.onChangeField(event, 'published');
													  logger.endLog();
												  }
												  
						  
												  
											  });
      var blogPost = new BlogPost(data);
      logger.log('Blog post was created from json data');
      var blogPostView = new BlogPostView({
											  model: blogPost
										  });
      //connect BlogPostView with dom
      $('#blogPostMainForm').append(blogPostView.render().el);
      //connect buttons
      $('#okButton').click(function () {
							   _.defer(function () {
										   blogPostView.onOKPressed();
									   });
						   });
      $('#cancelButton').click(function () {
								   blogPostView.onCancelPressed();
			       });
      $('#' + domManipulator.getId('title')).keyup(_.throttle(function (event) {
								  document.getElementById(domManipulator.getId("slug")).value = URLify(this.value, 200);
															  }, 100));
      //print scope leaks
      if (scopeleaks.leaks().toString()) {
          logger.log("Global Names = " + scopeleaks.leaks().toString());
      }
      logger.endLog();
  });
