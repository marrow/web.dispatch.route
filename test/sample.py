# encoding: utf-8

from web.dispatch.route import route


class Root(object):
	__slots__ = ['_ctx']
	
	def __init__(self, context=None):
		self._ctx = context
	
	@route('/user')  # These just set fn.__route__ to this value.
	def root(self):
		return "I'm all people."
	
	@route('/user/{username}')
	def user(self, username):
		return "Hi, I'm " + username
	
	@route('/user/{username}/action')
	def action(self, username):
		return "I'm also " + username
