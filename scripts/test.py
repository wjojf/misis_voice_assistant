from spider import WebSpider

method_list = [func for func in dir(WebSpider) if callable(getattr(WebSpider, func))]
method_list = [x for x in method_list if '__' not in x]
print(method_list)