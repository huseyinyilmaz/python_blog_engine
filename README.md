Python Blog Engine
==================

Introduction
------------
This blog engine that can serve multiple blogs from one instance which offers a lot more like db backed static pages , simple db backed menu, comments for blog post with gravatar support, markdown support for blog entries etc. 

* This project facilitates a base structure for a blog/personal website. Python blog engine can serve multiple blogs, static pages that stored on database.
* It is easy to use and very light weight web application. You can do changes you desire just changing the code if your really need to.
* Python blog engine uses markdown for its posts. So after your design phase is done you wont have to deal with html any more.
* You can serve multiple blogs with one deployment.
* With static page support, you can serve static pages without touching the deployment. Static pages are stored in database.
* With internal menu structure you can change application menu from admin interface.
* All front-end can be cached by memcache which will take db access to minimum.

Installation Notes
------------------
In order to use markdown, You must install following packages on your system

1. Install ElementsTree
   		   easy_install ElementTree
2. Install MarkDown
		   easy_install markdown
3. Install  Pygments
   			easy_install Pygments

