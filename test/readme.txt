bonjour 

list all services
dns-sd  -B  _services._dns-sd._udp

register a service 
dns-sd -R mytest _mytest._tcp local 21173

list a service by name
dns-sd  -B  _mytest._tcp

get service instance info
dns-sd  -L mytest  _mytest._tcp

get host name ip
dns-sd  -G v4v6 DESKTOP-NI68R3B.local.

register service
dns-sd -R mywebservice _http._tcp local 21173 key1=value1 key2=value2
