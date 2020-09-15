import requests
import re
import csv

def sqlInjectionTest(url):
  """
  SQL Injection test.
  
  Arguments:
  url: url to try the attack on in pattern 'METHOD URL'
       For instance, GET http://mywebsite.com/endpoint?query=

  Returns:
    True: TEST PASS, attack failed
    False: TEST FAILED, attack was successful, sql injected
  """
  STR_TO_INJECT = '\' | case randomblob(10000000) when not null then "" else "" end | \''

  urlSplit = url.split(' ')
  method = str(urlSplit[0]).lower()
  endpoint = str(urlSplit[1])

  if method == 'post':
    r = requests.post(endpoint + 'test')
    normal_elapsed_time = r.elapsed.microseconds + r.elapsed.seconds*1000000

    r = requests.post(endpoint + STR_TO_INJECT)
    injection_elapsed_time = r.elapsed.microseconds + r.elapsed.seconds*1000000
  else:
    r = requests.get(endpoint + 'test')
    normal_elapsed_time = r.elapsed.microseconds + r.elapsed.seconds*1000000

    r = requests.get(endpoint + STR_TO_INJECT)
    injection_elapsed_time = r.elapsed.microseconds + r.elapsed.seconds*1000000

  if(injection_elapsed_time > 5*normal_elapsed_time):
    return False
  else:
    return True

def fileDisclosureTest(url):
  """
  File Disclosure test

  Arguments:
  url: url to try the attack on in pattern 'METHOD URL'
       For instance, GET http://mywebsite.com/endpoint

  Returns:
    True: TEST PASS, attack failed
    False: TEST FAILED, attack was successful, file found
  """

  urlSplit = url.split(' ')
  method = str(urlSplit[0]).lower()
  endpoint = str(urlSplit[1])

  if method == 'post':
    return requests.post(endpoint).status_code != 200
  else:
    return requests.get(endpoint).status_code != 200

def ipAddressDisclosureTest(url):
  """
  IP Address Disclosure test

  Arguments:
  url: url to try the attack on in pattern 'METHOD URL'
       For instance, GET http://mywebsite.com/endpoint

  Returns:
    True: TEST PASS, attack failed
    False: TEST FAILED, attack was successful, at least 1 IP addr found
  """

  ipAddressRegex = '((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))'

  urlSplit = url.split(' ')
  method = str(urlSplit[0]).lower()
  endpoint = str(urlSplit[1])

  try:
    if method == 'post':
      testText = requests.post(endpoint).text
    else:
      testText = requests.get(endpoint).text
  except:
    raise ValueError('Unable to perform ' + str(url) )

  return re.search(ipAddressRegex, testText) == None