*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  hahaha
    Set Password  hahaha123
    Set Password Confirmation  hahaha123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ha
    Set Password  hahaha12
    Set Password Confirmation  hahaha12
    Click Button  Register
    Register Should Fail With Message  Username is too short, must be atleast 3 characters

Register With Valid Username And Too Short Password
    Set Username  jee
    Set Password  jee1
    Set Password Confirmation  jee1
    Click Button  Register
    Register Should Fail With Message  Password is too short, must be atleast 8 characters


Register With Valid Username And Invalid Password
    Set Username  jee
    Set Password  moimoimoi
    Set Password Confirmation  moimoimoi
    Click Button  Register
    Register Should Fail With Message  Password is too weak, must contain atleast 1 number or special character

Register With Nonmatching Password And Password Confirmation
    Set Username  jee
    Set Password  jeejee123
    Set Password Confirmation  jeejee12
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password} 


*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
