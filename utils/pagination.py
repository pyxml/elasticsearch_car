class Pagination:

	def __init__(self, page, all_count, per_num=15, max_show=5):
		try:
			page = int(page)
			if page <= 0:
				page = 1
		except Exception as e:
			page = 1

		self.page = page
		self.all_count = all_count
		self.per_num = per_num
		self.max_show = max_show
		# 总页码数
		self.page_num, more = divmod(all_count, per_num)
		if more:
			self.page_num += 1
		# 最多显示页码数
		half_show = max_show // 2

		if self.page_num < max_show:
			# 总页码数不够 最大显示页码数
			self.page_start = 1
			self.page_end = self.page_num
		else:
			# 能显示超过最大显示页码数
			if page <= half_show:
				# 处理左边的极值
				self.page_start = 1
				self.page_end = max_show
			elif page + half_show > self.page_num:
				# 处理右边的极值
				self.page_start = self.page_num - max_show + 1
				self.page_end = self.page_num
			else:
				# 正常的情况
				self.page_start = page - half_show
				self.page_end = page + half_show

	@property
	def start(self):
		return (self.page - 1) * self.per_num

	@property
	def end(self):
		return self.page * self.per_num

	@property
	def page_html(self):
		li_str = ''

		# 上一页
		if self.page == 1:
			li_str += '<li class="paginate_button disabled" ><a> << </a></li>'
		else:
			li_str += '<li ><a  page={}> << </a></li>'.format(self.page - 1)

		for i in range(self.page_start, self.page_end + 1):
			if self.page == i:
				li_str += '<li class="paginate_button active"><a  page={0}>{0}</a></li>'.format(i)
			else:
				li_str += '<li><a page={0}>{0}</a></li>'.format(i)
		# 下一页
		if self.page == self.page_num:
			li_str += '<li class="paginate_button disabled" ><a> >> </a></li>'
		else:
			li_str += '<li ><a page={}> >> </a></li>'.format(self.page + 1)

		return li_str
