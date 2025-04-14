Feature: Credit Application Flow

  Scenario: Reject if identity verification fails
    Given applicant provides fraudulent identity
    When process application is called
    Then application should be rejected with identity error

  Scenario: Accept valid applicant
    Given applicant provides valid identity
    When process application is called
    Then application should be approved with interest rate