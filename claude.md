# Create automation for web testing of a transaction processing application

## Technology 
* application - javascript , html , angular 
* backend - python based . exposes rest apis 
* communication - rest apis 
* database - sql lite

## Frontend 
* login screen - with user name , password .
  user name : demo 
  password  : password 
  should open the application 
* payment screen - post successful login , payment screen is visible
  Following fields on screen 
  1 Debtor 
  2 Creditor 
  3 amount 
  4 submit button .
  When user will press submit button , it will call REST end point /payment and get success and display transaction id

## REST api 
* /login end point 
* /payment end point

## Automation 
* playright tool

## Input data 
Refer to metadata.json while choosing input data 
I want to use sql-lite database later for fetching relevant data 