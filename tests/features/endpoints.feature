Feature: Sheriff API endpoints

  Scenario: Health check returns OK
    When I GET "/health"
    Then the response status code should be 200
    And the response JSON should be:
      """
      {"status":"ok"}
      """

  Scenario: Create recipient with valid data
    Given a valid recipient payload
    When I POST "/create_recipient" with the payload
    Then the response status code should be 200
    And the response should contain "account_id"
    And the response should contain "onboarding_link"

  Scenario: List recipients
    When I GET "/recipients"
    Then the response status code should be 200
    And the response should contain "recipients"
