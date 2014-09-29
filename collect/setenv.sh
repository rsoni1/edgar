# source this file for setting env varibales to use with coreutils on Mac OS X

>|testsort
sort -R testsort >/dev/null 2>&1 || echo "sort -R unsupported"
rm testsort

# Download and install coreutils
export PATH="$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:$PATH"
>|testsort
sort -R testsort >/dev/null 2>&1 || echo "sort -R still unsupported"
rm testsort
