Feature: E2E Product Purchase
  As an authenticated user
  I want to add a product to the cart and checkout
  So that I can complete my purchase order successfully

  Scenario: End to End Product Purchase
    Given I am a logged-in user on the inventory page
    When I add the backpack to the cart and proceed to checkout
    And I fill in the checkout information
    Then the order should be finalized with a success message
