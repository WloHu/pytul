def sum_range(*args):
	if len(args) == 1:
		return _sum_range_limit(*args)
	elif 1 < len(args) < 4:
		return _sum_range_full(*args)
	raise TypeError("sum_range takes 1 to 3 arguments ({} given)".format(len(args)))

def _sum_range_limit(stop):
	return stop * (stop+1) / 2
	
def _sum_range_full(start, stop, step=None):
	if step:
		return _sum_range_full(start // step, stop // step) * step
	return _sum_range_limit(stop) - _sum_range_limit(start)