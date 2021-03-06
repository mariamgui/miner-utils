import unittest
from minerutils import GitHub

class GitHubTest(unittest.TestCase):

	def setUp(self):
		self.g = GitHub()

	def tearDown(self):
		self.g = None

	def test_repo_exists(self):
		self.assertTrue(self.g.repoExists("caiusb", "github-utils"))

	def test_repo_doesnt_exit(self):
		self.assertFalse(self.g.repoExists("caiusb", "invalid"))

	def test_rate_limit(self):
		if (self.g.usesAuth()):
			limit = 5000
		else:
			limit = 60
		self.assertTrue(self.g.getRemainingRateLimit() <= limit)

	def test_paginated_call(self):
		reposNo = len(self.g.get('users/caiusb/repos', perPage=10))
		self.assertTrue(reposNo >= 47)

	def test_headers(self):
		stargazers = self.g.get('/repos/caiusb/gitective/stargazers', headers={'Accept': 'application/vnd.github.v3.star+json'})
		self.assertTrue(len(stargazers) > 0)
		self.assertTrue(len(stargazers[0].keys()) == 2)

	def test_follow_links(self):
		repo = self.g.get('/repos/caiusb/gitective')
		forks = self.g.get(repo['forks_url'])
		self.assertTrue(len(forks) > 0)

	def test_search_api(self):
		users = self.g.get('/search/users', params={'q': 'caiusb'})
		self.assertTrue(len(users) > 0)

	def test_url_params(self):
		users = self.g.get('/search/users?q=caiusb')
		self.assertTrue(len(users) > 0)

if __name__ == '__main__':
	unittest.main()
