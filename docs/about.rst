=================
About pillowncase
=================

pillowncase is an experiment in hiding data in images, I had some time over the winter break and wanted to try and create a small python project end to end.

----------------
How does it work
----------------

pillowncase takes any source file and then splits it up hiding the data in the low end bits of each pixel.  It takes advantage of the fact that PNG images are lossless, this would not work with JPG.

You can define how granular you want to break the data up and across which channels (RGBA) each pixel can hold a value between 0 and 255 for each channel in the format I'm using.  I am masking off the low end bits and spreading the data across each pixel.  The more bits replaced the less of the original image is left but the smaller the file, the less bits replaced the less you will notice the file has changed.

Have a play about with it, it's easier to see, I've included plenty of examples in the code.

----------
Next Steps
----------

It's slow at the moment because I'm using Python to iterate over each pixel and doing lots of int to binary strings etc.  It's just a proof of concept.

Next steps are speeding the adding and extracting data up using numpy most likely and if that's not quick enough I'll look to multi thread it.

After that I'm going to have a go at doing a GUI.

have a look through the rest of the documentation and code and feel free to fork it.