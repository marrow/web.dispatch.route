# encoding: utf-8


def route(route, router=None):
	def inner(func):
		if router:
			# Immediate routing declaration; mostly for testing.
			router.register(route, func)
		else:
			# Deferred routing declaration.
			func.__route__ = route
		return func
	
	return inner
