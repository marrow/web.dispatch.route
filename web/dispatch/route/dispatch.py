# encoding: utf-8

from inspect import isclass

from .router import Router


class RouteDispatch(object):
	def __init__(self, config):
		super(RoutingDialect, self).__init__()
	
	def __call__(self, context, root):
		log = context.log
		path = context.request.remainder
		
		# Capture and eliminate the final, empty path element.
		# If present there was a trailing slash in the original path, which we don't care about.
		if path[-1:] == ['']:
			path.pop()
		
		path = unicode(path)
		
		if isclass(root):
			# Build a strongly-bound router for this object.
			# If you add new routes during method calls, pass self.__router__ as a second argument to
			# the @route decorator to ensure your route is discoverable.
			root = root(context)
			
			if not hasattr(root, '__router__'):
				router = root.__router__ = Router()
				
				for name in (i for i in dir(root) if not i.startswith('_')):
					obj = getattr(root, name)
					route =  getattr(obj, '__route__', None)
					if not route: continue
					router.register(route, obj)
		
		try:
			target, remainder, args = router.route(path)
			remainder = '/' + '/'.join(remainder)
			context.request.kwargs.update(args)
		
		except ValueError as e:
			raise HTTPNotFound()
		
		yield path[:len(path)-len(remainder)].split('/'), target, not hasattr(target, '__dialect__')
