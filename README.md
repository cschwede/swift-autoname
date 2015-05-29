Openstack Swift AutoName Middleware
=========================================

``autoname`` is a middleware that automaticall generates objectnames using uuids
if a PUT request is send to Swift including a containername and a trailing
slash, but no object name. The chosen objectname is returned in the response
header ``X-Object-Meta-Public-Autoname```.

Current status
--------------
Proof of concept. Don't use in production yet!

Quick Install
-------------

1) Install autoname:

    git clone git://github.com/cschwede/swift-autoname.git
    cd swift-autoname
    sudo python setup.py install

2) Add a filter entry for autoname to your proxy-server.conf:
  
    [filter:autoname]
    use = egg:autoname#autoname

3) Alter your proxy-server.conf pipeline and add autoname:

    [pipeline:main]
    pipeline = catch_errors healthcheck cache autoname tempauth proxy-server

4) Restart your proxy server: 

    swift-init proxy reload

Done!


Example use
-----------

Using curl and python-swiftclient:

    > curl -H "X-Auth-Token: AUTH_token" -i -v -X PUT --data @filename http://saio:8080/v1/AUTH_test/containername/
    < ...
    < X-Object-Meta-Public-Autoname: 17c73a89-5e18-48ba-8f41-88b7dad817ec
    < ...
    > swift list containername
    < ...
    < 17c73a89-5e18-48ba-8f41-88b7dad817ec
