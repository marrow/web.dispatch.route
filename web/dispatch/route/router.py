# encoding: utf-8

import re

re_type = type(re.compile(""))


class Router(object):
	def __init__(self):
		self.routes = list()
	
	def register(self, route, obj):
		parsed = self.parse(route)
		
		routes = self.routes
		
		for element in parsed:
			for i, (route, children) in enumerate(routes):
				if route is not element:
					continue
				
				if not isinstance(children, list):
					children = [(None, children)]
					routes[i] = (route, children)
				
				routes = children
				break
			
			else:
				routes.append((element, obj))
	
	def parse(self, route):
		parts = route.lstrip('/').split('/')
		
		for i, part in enumerate(parts):
			if '{' not in part:
				continue
			
			elif '}' not in part:
				raise ValueError("Route match must not contain forward slashes.")
			
			sub = list()
			
			while part:
				prefix, _, match = part.partition('{')
				name, _, part = match.partition('}')
				sub.append(prefix)
				
				name, _, regex = name.partition(':')
				sub.append('(?P<%s>%s)' % (name, regex or r'[^/]+'))
			
			parts[i] = re.compile(''.join(sub))
		
		return parts
	
	def route(self, path):
		routes = self.routes
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
