#!/usr/bin/env python3
"""
Unit tests for client module.

This module contains unit tests for the GithubOrgClient class
using the unittest framework with parameterized testing and mocking.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repository names.

        This test mocks both get_json and _public_repos_url to verify that
        public_repos correctly processes the payload and returns repo names.
        
        Args:
            mock_get_json: Mocked get_json function
        """
        # Define the payload that get_json will return
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = mock_repos_payload
        
        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url',
                         new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/test/repos"
            )
            
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            
            # Expected result: list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            
            # Verify that _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()
            
            # Verify that get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns the expected boolean value.

        This test verifies that the static method has_license correctly
        compares the license key from the repo with the given license_key.

        Args:
            repo (dict): Repository data with license information
            license_key (str): License key to check for
            expected (bool): Expected return value
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(
        fixtures.org_payload,
        fixtures.repos_payload,
        fixtures.expected_repos,
        fixtures.apache2_repos
    )]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.

    This class performs integration tests using real fixture data
    to test the complete workflow of GithubOrgClient without making
    actual HTTP requests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class fixtures before running integration tests.

        This method mocks requests.get to return predefined payloads
        based on the URL being requested, allowing integration tests
        to run without making actual HTTP calls.
        """
        def side_effect(url):
            """
            Side effect function for mocking requests.get.

            Args:
                url (str): The URL being requested

            Returns:
                Mock object with json method returning appropriate payload
            """
            from unittest.mock import Mock
            
            mock_response = Mock()
            if url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            elif "orgs/" in url:
                mock_response.json.return_value = cls.org_payload
            else:
                mock_response.json.return_value = {}
            
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after integration tests.

        This method stops the requests.get patcher to restore
        normal HTTP functionality.
        """
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()