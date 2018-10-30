# httpcs
Implement HTTP sockets using python

## Client (httpc)

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

## Server (httpf)

- python -m httpf -v -p 3038

- python -m httpf -v -p 3038 -d 'new_directory/'

Note that the root directory is set to `-d`, and by default it is `file/`

*Testing with httpc

- python -m httpc get -v 'http://localhost:3038'

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/nonexist.txt' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/test.txt' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/test.json' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/test.html' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/test.xml' 

- python -m httpc get -v -H ACCESS:xml 'http://localhost:3038/test.bin' 

- python -m httpc post -v --d 'this is to test if the post request is good.' 'http://localhost:3038/test_post.txt' 

- python -m httpc post -v --d 'this is to test if the post request is good.' 'http://localhost:3038/deep/test_post.txt' 

- python -m httpc post -v --d 'this is to test if the post request is good.' 'http://localhost:3038/test.txt' 

- python -m httpc post -v --d 'this is to test if the post request is good.' 'http://localhost:3038/' 
