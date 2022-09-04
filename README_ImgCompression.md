## Usage of Daisi

It is recommended to use this application on the daisi platform itself using the link https://app.daisi.io/daisies/vijay/Image%20Compression/api. However, you can still use your own editor using the below method:

### First, load the Packages:

```
import pydaisi as pyd
image_compression = pyd.Daisi("vijay/Image Compression")
```

## Now, connect to Daisi and access the functions using the following functions:

### Load Image:

```
image_compression.load_image(image_file).value
```

### Compress Image:

```
image_compression.compression(img).value
```

### Binary Search:

```
image_compression.binarySearch(encode, l, h, x).value
```

returns index if present and -1 if not present

### Image Flattening:

```
image_compression.flatten_image(image).value
```

flattens an image from 2d to 1d array

### SNR:

```
image_compression.SNR(original_img, compressed_img, rows, cols).value
```

shows difference between original img and compressed img

## And done! We have compressed our image!
