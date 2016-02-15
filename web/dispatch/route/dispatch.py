# encoding: utf-8

from inspect import isclass

from .router import Router

if __debug__:
	import warnings
	from collections import deque

try:
	str = unicode
except:
	str = str


class RouteDispatch(object):
	def __init__(self, config):
		super(RouteDispatch, self).__init__()
	
	def __call__(self, context, obj, path):
		if __debug__:
			if not isinstance(path, deque):
				warnings.warn(
						"Your code uses auto-casting of paths to a deque; "
						"this will explode gloriously if run in a production environment.",
						RuntimeWarning, stacklevel=1
					)
				
				if isinstance(path, str):
					path = deque(path.split('/')[1 if not path or path.startswith('/') else 0:])
				else:
					path = deque(path)
			
			log.debug("Preparing route dispatch.", extra=dict(
					dispatcher = repr(self),
					context = repr(context),
					obj = repr(obj),
					path = list(path)
				))
		
		if isclass(obj): # Build a strongly-bound router for this object.
			obj = obj() if context is None else obj(context)
			yield None, obj, False  # Let everyone know we instantiated something.
			
			obj = router.from_object(obj)
			yield None, obj, False  # Let everyone know we're switching to the router.
		
		def route(self, path):
			routes = self.data
			path = path.lstrip('/').split('/') + [None]
			match = dict()
			
			for i, element in enumerate(path):
				for route, children in routes:
					if isinstance(route, re_type):
						matched = route.match(element)
						if not matched: continue
						match.update(matched.groupdict())
					
					elif route != element:
						continue
					
					if not isinstance(children, list):
						return children, [i for i in path[i+1:] if i is not None], match
					
					routes = children
					break
				
				else:
					raise ValueError("Could not find route to satisfy path.")
			
			raise ValueError("Could not find route to satisfy path.")
		
			
		
		
		try:
			target, remainder, args = router.route(path)
			remainder = '/' + '/'.join(remainder)
			context.request.kwargs.update(args)
		
		except ValueError as e:
			raise HTTPNotFound()
		
		yield path[:len(path)-len(remainder)].split('/'), target, not hasattr(target, '__dialect__')
