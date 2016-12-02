#!/bin/bash

# Grab a copy of the Oracle 8 JDK. There has got to be a better way to do this.

if [ ! -f el6-src/jdk-8u111-linux-x64.rpm ]; then
    echo "Getting Oracle 8 JDK..."
    curl -v -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.rpm > el6-src/jdk-8u111-linux-x64.rpm
fi

