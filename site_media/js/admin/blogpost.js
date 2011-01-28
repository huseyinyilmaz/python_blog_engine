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
      var WidgetView = Backbone.View.extend({
												tagName: 'li',
												template: _.template($('#template_tag').html())
												
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
																this.url = options.url;
																this.each(function(model){
																			  model.url = options.model_url;
																		  });
																delete options.url;
																delete options.model_url;
																logger.endLog();
															}
															
														});
      var Widget = Backbone.View.extend({
											//el : $()get in initialization
											//title:get in initialization
											//list : get in initialization
											template: _.template($('#template_side_widget').html()),
											events: {},
											initialize: function (options) {
												logger.startLog('TagWidget.initialize');
												//this.title = options.title;
												var widgetHtml = domManipulator.side_widget({title: options.title});
												delete options.title;
												logger.endLog();
											},
											render: function () {
												logger.startLog('TagWidget.render');
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
												   var tagCollection = new WidgetCollection(this.get("tags"),
																							{url:'admin/tags',
												  											 model_url:'blobla'});

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
												   
												   var tagWidget = new Widget({
																				  el: $("tag_widget"),
																				  url: 'admin/bla',
																				  title: 'Tags',
																				  list: this.tags
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
