
# collager

A collage tool in python

## usage

create file, then follow these steps:

first, list each image path you would like to use. seperate by line.

follow by two newlines, then mark up the table. 

```
d:\pictures\1.png
d:\pictures\2.png
d:\pictures\3.png

 0 - 2
 1 - |
```

numbers indicate an image in the location. dashes (`-`) indicate that the image before it will span one more tile horizontally. these can be use infinitely. pipes (`|`) indicate that the image above it will span one more tile vertically downward. these can also be used infinitely.

the extra spaces are important, don't leave them out.
