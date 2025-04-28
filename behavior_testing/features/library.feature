Feature: Washington County Library website functionalities
  As a library user
  I want to browse the library website
  So that I can access library services and information.
  @skip
  Scenario: Check if the address is correct 
    Given I navigate to "https://library.washco.utah.gov/"
    When I am on the main Washington County branch page
    Then I should see the address
  @skip
  Scenario: Check the branch manager for the St. George branch
    Given I navigate to "https://library.washco.utah.gov/"
    When I navigate to the St. George branch
    Then I should see the branch manager
  @skip
  Scenario: Navigate to the Renew/Pay Fines login page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the "Renew/Pay Fines" tab
    Then I should see a login page
  @skip
  Scenario: Check if rooms are available
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the Library Programs link in the Book A Room drop down menu
    Then I should be on the book a room page
  @skip
  Scenario: Navigate to monthly newsletters page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the Monthly Newsletters link in the Whats New drop down menu
    Then I should see the newsletters headline
  @skip
  Scenario: Navigate to book catalog page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the Search The Online Catalog link in the Catalog drop down menu
    Then I should be on the online catalog page
    
  Scenario: Search for book on catalog page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the Search The Online Catalog link in the Catalog drop down menu
    And I search the catalog for Twilight
    Then Twilight should be in the search results
 
  Scenario: Navigate to Mission and History page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click on the Mission & History link in the More drop down menu
    Then I should see the Mission & History header
  
  Scenario: Navigate to Saint George library book club page
    Given I navigate to "https://library.washco.utah.gov/"
    When I click the Page Turners Club link in the Saint George Community drop down menu
    Then I should see the book club page header
  
  Scenario: Check the contct information for the board of directors 
    Given I navigate to "https://library.washco.utah.gov/"
    When I click the Board of Directors link in the More drop down menu
    Then I should see the contact information for the board of directors
