from skimage.transform import pyramid_gaussian
from PIL import Image
import cv2

im = cv2.imread("../data/images/robben.jpg")
min_wdw_sz = (100, 100)
step_size = (50, 50)
downscale = 1.25

def sliding_window(image, window_size, step_size):
    '''
    This function returns a patch of the input image `image` of size equal
    to `window_size`. The first image returned top-left co-ordinates (0, 0) 
    and are increment in both x and y directions by the `step_size` supplied.
    So, the input parameters are -
    * `image` - Input Image
    * `window_size` - Size of Sliding Window
    * `step_size` - Incremented Size of Window

    The function returns a tuple -
    (x, y, im_window)
    where
    * x is the top-left x co-ordinate
    * y is the top-left y co-ordinate
    * im_window is the sliding window image
    '''
    for y in xrange(0, image.shape[0], step_size[1]):
        for x in xrange(0, image.shape[1], step_size[0]):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

for im_scaled in pyramid_gaussian(im, downscale=downscale):
    if im_scaled.shape[0] < min_wdw_sz[0] or im_scaled.shape[1] < min_wdw_sz[1]:
        break
    for (x, y, im_window) in sliding_window(im_scaled, min_wdw_sz, step_size):
        if im_window.shape[0] != min_wdw_sz[1] or im_window.shape[1] != min_wdw_sz[0]:
            continue
        clone = im_scaled.copy()
        cv2.rectangle(clone, (x, y), (x + im_window.shape[1], y + im_window.shape[0]), (255, 255, 255))
        cv2.imshow("Image", clone)
        cv2.waitKey(30)
