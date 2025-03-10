# Implement By - @VarnaX-279

import time
import string
import random
import logging

from telegraph import Telegraph
from telegraph.exceptions import RetryAfterError

from bot import LOGGER


class TelegraphHelper:
	def __init__(self, author_name=None, author_url=None):
		self.telegraph = Telegraph()
		self.short_name = ''.join(random.SystemRandom().choices(string.ascii_letters, k=8))
		self.access_token = None
		self.author_name = author_name
		self.author_url = author_url
		self.create_account()

	def create_account(self):
		self.telegraph.create_account(
			short_name=self.short_name,
			author_name=self.author_name,
			author_url=self.author_url
		)
		self.access_token = self.telegraph.get_access_token()
		LOGGER.info(f"Creating TELEGRAPH Account using  '{self.short_name}' name")

	def create_page(self, title, content):
		try:
			return self.telegraph.create_page(
				title = title,
				author_name=self.author_name,
				author_url=self.author_url,
				html_content=content
			)
		except RetryAfterError as st:
			LOGGER.warning(f'Telegraph Flood control exceeded. I will sleep for {st.retry_after} seconds.')
			time.sleep(st.retry_after)
			return self.create_page(title, content)

	def edit_page(self, path, title, content):
		try:
			return self.telegraph.edit_page(
				path = path,
				title = title,
				author_name=self.author_name,
				author_url=self.author_url,
				html_content=content
			)
		except RetryAfterError as st:
			LOGGER.warning(f'Telegraph Flood control exceeded. I will sleep for {st.retry_after} seconds.')
			time.sleep(st.retry_after)
			return self.edit_page(path, title, content)


telegraph=TelegraphHelper('Mirror-Leech-Telegram-Bot', 'https://t.me/Masterrzzz')
