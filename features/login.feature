Feature: User Authentication
  As a registered user
  I want to log into the SauceDemo application
  So that I can access my inventory dashboard

  Scenario: Successful Login with Valid Credentials
    Given I navigate to the login page
    When I enter a valid username and password
    Then I should be redirected to the inventory page

  Scenario Outline: Failed Login with Invalid Credentials
    Given I navigate to the login page
    When I enter an invalid username <username> and password <password>
    Then I should see the login error message <expected_error>

    Examples:

      | username        | password         | expected_error                                                            |
      | invalid_user    | invalid_password | Epic sadface: Username and password do not match any user in this service |
      | standard_user   | invalid_password | Epic sadface: Username and password do not match any user in this service |
      |                 |                  | Epic sadface: Username is required                                        |
      | locked_out_user | secret_sauce     | Epic sadface: Sorry, this user has been locked out.                       |

