
# pod_whois
A [babashka pod](https://github.com/babashka/babashka.pods) for whois query.

Implemented using the Python [python-whois](https://pypi.org/project/python-whois/) and [ipwhois](https://pypi.org/project/ipwhois/) library.

## Status

Experimental.

## Usage

install this package from pip:
```sh
pip install pod-whois
```

Load the pod:

```clojure
(require '[babashka.pods :as pods])
(babashka.pods/load-pod "pod.py-whois")

(pod.py-whois/query "www.bing.com")
(pod.py-whois/query "8.8.8.8")
```

## Build 

require python >= 3.6, install deps

```sh
pip install -r dev-requirements.txt
pip install -r requirements.txt

./reinstall
```

## License

Copyright © 2021 ntestoc3
