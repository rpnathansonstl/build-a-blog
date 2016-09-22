#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
from google.appengine.ext import db
import re
#contains get_by_id function
# from datetime import datetime
# import hashutils

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# class User(db.Model):
#     """ Represents a user on our site """
#     username = db.StringProperty(required = True)
#     pw_hash = db.StringProperty(required = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render_front()
        # self.render("front.html", title=title, entry=entry, error=error, entries=entries)
        # # self.render_front()

    def render_front(self, title="", entry="", error=""):
    # def render_front(self, title="", author="", entry="", error=""):
        entries = db.GqlQuery("SELECT * FROM Entry ORDER by created DESC LIMIT 5")

        self.render("front.html", title=title, entry=entry, error=error, entries = entries)
        # self.render("front.html", title=title, author=author, entry=entry, error=error, entries = entries)

class Entry(db.Model):
    title = db.StringProperty(required = True)
    # author = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class NewEntry(Handler):
    def get(self):
        self.render_front()
        # entries = db.GqlQuery("SELECT * FROM Entry ORDER by created DESC LIMIT 5")
        # self.render("post.html", title=title, entry=entry, error=error, entries=entries)

    def render_front(self, title="", entry="", error=""):
        # def render_front(self, title="", author="", entry="", error=""):
        entries = db.GqlQuery("SELECT * FROM Entry ORDER by created DESC LIMIT 5")

        self.render("post.html", title=title, entry=entry, error=error, entries = entries)
        # self.render_front()

    def post(self):
        title = self.request.get("title")
        # title = self.request.get("author")
        entry = self.request.get("entry")

        if title and entry:
        # if title and author and entry:
            a = Entry(title = title, entry = entry)
            # a = Entry(title = title, author = author, entry = entry)
            a.put()
            self.redirect("/blog")
        else:
            error = "Please include a title and an entry."
            self.render_front(title, entry, error)
            # self.render_front(title, author, entry, error)

class ViewPostHandler(Handler):
    def get(self, id):
        Stored=Entry.get_by_id(int(id))
        self.render("stored.html", entry=Stored)

app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/new', NewEntry),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
