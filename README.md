# httpc
Implement HTTP sockets using python

- GET/POST
- Support file upload for POST
- Support verbose option
- Support redirect
- Support export


Test sets:

- python -m httpc -h
- python -m httpc get -h
- python -m httpc post -h

- python -m httpc get http://httpbin.org/get?course=networking&assignment=1
- python -m httpc get -v http://httpbin.org/get?course=networking&assignment=1 
- python -m httpc get -v -o http://httpbin.org/get?course=networking&assignment=1 

- python -m httpc post http://httpbin.org/post
- python -m httpc post -v http://httpbin.org/post
- python -m httpc post -v -o http://httpbin.org/post
- python -m httpc post -v -H Content-Type:application/json http://httpbin.org/post
- python -m httpc post -v -H Content-Type:application/json --d '{"hello":"It's me"}'http://httpbin.org/post
- python -m httpc post -v -H Content-Type:application/json -f test.json http://httpbin.org/post