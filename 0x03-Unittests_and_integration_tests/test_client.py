#!/usr/bin/env python3
"""
Unit tests for client module.

This module contains unit tests for the GithubOrgClient class
using the unittest framework with parameterized testing and mocking.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for GithubOrgClient.

    This class contains unit tests to verify that GithubOrgClient
    correctly retrieves organization data from the GitHub API.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name):
        """
        Test that GithubOrgClient.org returns the correct value.

        This test ensures that the org property calls get_json with the
        correct URL and returns the expected result without making actual
        HTTP requests.

        Args:
            org_name (str): The organization name to test
        """
        test_payload = {"login": org_name, "id": 12345}
        
        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = test_payload
            client = GithubOrgClient(org_name)
            
            # Clear any memoize cache if it exists
            if hasattr(client, '_memoize_cache'):
                client._memoize_cache.clear()
            
            result = client.org
            expected_url = f"https://api.github.com/orgs/{org_name}"
            
            self.assertEqual(result, test_payload)
            mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the expected URL.

        This test uses patch as a context manager to mock the org property
        and verify that _public_repos_url returns the repos_url from the
        mocked payload.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }
        
        with patch.object(GithubOrgClient, 'org', 
                         new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("test-org")
            result = client._public_repos_url
            
            self.assertEqual(result, mock_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()