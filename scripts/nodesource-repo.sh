#!/bin/bash
# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
set -euo pipefail

NODE_VERSION="$1"
NODESOURCE_DIR="$(echo "$NODE_VERSION" | awk -F. '{ if ($1 == "0") { print "pub_" $1 "." $2 } else { print "pub_" $1 ".x" } }')"
NODESOURCE_BASEURL="${NODESOURCE_BASEURL:-https://rpm.nodesource.com/$NODESOURCE_DIR/el}"
NODESOURCE_KEY=/etc/pki/rpm-gpg/NODESOURCE-GPG-SIGNING-KEY-EL

cat > $NODESOURCE_KEY <<EOF
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQINBFQCN9QBEADv5QYOlCWNkI/oKST/GGpQkOZjFY2cbYdHuc2j8kyM4oeNluXq
puEYMHOoQvbJ3DFPvsv+jCruL7qjkel9YzaF6e3RN2ystP4YBjxyOT7Bb5EnjNNU
6oScQJ50/+RmA4N3wzBrw5+x5KQGBfRU/k7JdDKO6SGY0zzdAo3jqp1nQ9Sf+Fmg
hsjDLVZTHorLPV3yPLb37QlvBB2YIRF+dL9l4wPAI/fGyWv+Qs7VlCZTyRAnKGbv
qN1LvlYoV9YqxaJYYJW+MQhn4706yNJAFeOZuKejEcnZTd/NBiAR91sVnsXKgW9e
yb4TZ7SqkmrJpuKJBpdPr1dgaK8dDmFh9Nlhpz6xZuYcKaDEDa5b3wymnixtwZf2
WyboChIlsHDajtXZt34xP9uUge1VHyk1o8AQUzKEpuepxxLnyXArLgvHaLhQnxPA
bQB43b4RbWYHPdB16ki2WoZX/DA4YEtfxg8GC3zXC2thMJnFburmts71iiYsxKBc
6d7O8415xrErhk2/o2+bRhf+7qBQfW0oxQSEMBYbqP3hvhG1VWc9umjbCfMgHrHo
IzI7W+GbRdbSsdpY6JNKuCftVfIKXeXk5FbUUP9NzsG/nyGFORkq9y0AKmocx3TD
w9DRG2SmKIKBOG5PQuzuXqsdUaYcFpySXdPNQG2CPtguPhQivw4qM3pQpQARAQAB
tCNOb2RlU291cmNlIDxncGctcnBtQG5vZGVzb3VyY2UuY29tPokCOAQTAQIAIgUC
VAI31AIbAwYLCQgHAwIGFQgCCQoLBBYCAwECHgECF4AACgkQXdvo1DT6dN2uaA//
UwKsmnz4MCH7Jn/vG0OinGQTfSH5uvlH68yOZmKLnhtfiqUq1gZz734S75ExxGP4
SGFYeK9CqKFgoGbpjzLLc5kvA7GdDX3E/exEjYa+GrJ9uIOUtaCKstTD5fPVj2Wf
TZtK9v1F6iYKyPHdJnSc5p7AxbLZkarF1CPJQWv2iDrg3dO3Oy41aazRwxJe9hvI
a//XavnsW2TTeo8qfQ0qrs8vzt8bxJF+PkACmqQfbXAiflCct5XEUbhbX1b8KznP
ppd5PLrvRTjHnZi/QRjky0qsUOukGiQhT6iZeiOUcLPeD+f7tA7JBZ08XXRfnLLj
mqYbIHPFG4C/AM5RXu5OdCtFrZQsJgGQEeg/UxYEz5qqNljKjRZ8XsmcyeWouKFM
LuVr1ORF6crl8lAdT3RujP2MzY8cvxJQesYKdWqk3bPXI7oG/PRReoeN86TqraYO
UeTssVlw5lmJtAH+eHt3K6TSjd0rq1RY7xWfttD7L8ECfPmBzbL54MSmKx9MBz+o
a9vOWQ2LjIbR/6DEyQiDpGhQTM+r0/SVS/kqR/j0SEHvOql+sn9sK1/qR1h3JtgI
6YF4IDXBE9s0RBCLbdxtVf3eAcbOnhkhefMtpURJLdVuU8HhMCiVUlHDUPHIuT5z
Lp+avdanIgi8Cnps/DpMI2KigEHW5mmqihXtfKj0jeE=
=9Bql
-----END PGP PUBLIC KEY BLOCK-----
EOF

cat > /etc/yum.repos.d/nodesource-el.repo <<EOF
[nodesource]
name=Node.js Packages for Enterprise Linux \$releasever - \$basearch
baseurl=${NODESOURCE_BASEURL}/\$releasever/\$basearch/
failovermethod=priority
enabled=1
gpgcheck=1
gpgkey=file://${NODESOURCE_KEY}

[nodesource-source]
name=Node.js for Enterprise Linux \$releasever - \$basearch - Source
baseurl=${NODESOURCE_BASEURL}/\$releasever/\$basearch/SRPMS
failovermethod=priority
enabled=0
gpgkey=file://${NODESOURCE_KEY}
gpgcheck=1
EOF
