import os, random, argparse
from PIL import Image
import imghdr
import numpy as np

def getAverageRGB(image):
  """
  Tìm giá trị trung bình (r, g, b) của ảnh
  """
  # get image as numpy array
  im = np.array(image)
  # get shape
  w,h,d = im.shape
  # get average
  return tuple(np.average(im.reshape(w*h, d), axis=0))

def splitImage(image, size):
  """
  Chia hình ảnh có kích thước m*n thành m*n hình ảnh
  """
  W, H = image.size[0], image.size[1]
  m, n = size
  w, h = int(W/n), int(H/m)
  # image list
  imgs = []
  # generate list of dimensions
  for j in range(m):
    for i in range(n):
      # append cropped image
      imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
  return imgs

def getImages(imageDir):
  """
  Đọc ảnh trong folder input
  """
  files = os.listdir(imageDir)
  images = []
  for file in files:
    filePath = os.path.abspath(os.path.join(imageDir, file))
    try:
      fp = open(filePath, "rb")
      im = Image.open(fp)
      images.append(im)
      im.load()
      fp.close()
    except:
      # skip
      print(f"Invalid image: {filePath}")
  return images

def getImageFilenames(imageDir):
  """
  Lấy danh sách tên của từng ảnh trong folder input
  """
  files = os.listdir(imageDir)
  filenames = []
  for file in files:
    filePath = os.path.abspath(os.path.join(imageDir, file))
    try:
      imgType = imghdr.what(filePath)
      if imgType:
        filenames.append(filePath)
    except:
      # skip
      print(f"Invalid image: {filePath}")
  return filenames

def getBestMatchIndex(input_avg, avgs):
  """
  Tìm index ảnh có giá trị RGB gần nhất với mỗi ô pixel
  """

  # input image average
  avg = input_avg

  # get the closest RGB value to input, based on x/y/z distance (RMSE)
  index = 0
  min_index = 0
  min_dist = float("inf")
  for val in avgs:
    # dist = (r1 - r2)^2 + (g1 - g2)^2 + (b1-b2)^2
    dist = ((val[0] - avg[0])*(val[0] - avg[0]) +
            (val[1] - avg[1])*(val[1] - avg[1]) +
            (val[2] - avg[2])*(val[2] - avg[2]))
    if dist < min_dist:
      min_dist = dist
      min_index = index
    index += 1

  return min_index


def createImageGrid(images, dims):
  """
  Từ ảnh mục tiêu có kích thước m*n, tạo ra grid m*n ô
  """
  m, n = dims

  assert m*n == len(images)

  width = max([img.size[0] for img in images])
  height = max([img.size[1] for img in images])

  # create output image
  grid_img = Image.new('RGB', (n*width, m*height))

  # paste images
  for index in range(len(images)):
    row = int(index/n)
    col = index - n*row
    grid_img.paste(images[index], (col*width, row*height))

  return grid_img


def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images=True):
  """
  Tạo ảnh mosaic
  """

  print('splitting input image...')
  # split target image
  target_images = splitImage(target_image, grid_size)

  print('finding image matches...')

  # for each target image, pick one from input
  output_images = []
  count = 0
  batch_size = int(len(target_images)/10)

  # calculate input image averages
  avgs = []
  for img in input_images:
    avgs.append(getAverageRGB(img))

  for img in target_images:
    # target sub-image average
    avg = getAverageRGB(img)
    # find match index
    match_index = getBestMatchIndex(avg, avgs)
    output_images.append(input_images[match_index])
    # user feedback
    if count > 0 and batch_size > 10 and count % batch_size == 0:
      print('processed %d of %d...' %(count, len(target_images)))
    count += 1
    # remove selected image from input if flag set
    if not reuse_images:
      input_images.remove(match_index)

  print('creating mosaic...')
  # draw mosaic to image
  mosaic_image = createImageGrid(output_images, grid_size)

  # return mosaic
  return mosaic_image

# Gather our code in a main() function
def main():
  # Command line args are in sys.argv[1], sys.argv[2] ..
  # sys.argv[0] is the script name itself and can be ignored

  # parse arguments
  parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
  # add arguments
  parser.add_argument('--target-image', dest='target_image', required=True)
  parser.add_argument('--input-folder', dest='input_folder', required=True)
  parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
  parser.add_argument('--output-file', dest='outfile', required=False)

  args = parser.parse_args()

  ###### INPUTS ######

  # target image
  target_image = Image.open(args.target_image)

  # input images
  print('reading input folder...')
  input_images = getImages(args.input_folder)

  # check if any valid input images found
  if input_images == []:
      print('No input images found in %s. Exiting.' % (args.input_folder, ))
      exit()

  # shuffle list - to get a more varied output?
  random.shuffle(input_images)

  # size of grid
  grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

  # output
  output_filename = 'mosaic.png'
  if args.outfile:
    output_filename = args.outfile

  # re-use any image in input
  reuse_images = True

  # resize the input to fit original image size?
  resize_input = True

  ##### END INPUTS #####

  print('starting photomosaic creation...')

  # if images can't be reused, ensure m*n <= num_of_images
  if not reuse_images:
    if grid_size[0]*grid_size[1] > len(input_images):
      print('grid size less than number of images')
      exit()

  # resizing input
  if resize_input:
    print('resizing images...')
    # for given grid size, compute max dims w,h of tiles
    dims = (int(target_image.size[0]/grid_size[1]),
            int(target_image.size[1]/grid_size[0]))
    print(f"max tile dims: {dims}")
    # resize
    for img in input_images:
      img.thumbnail(dims)

  # create photomosaic
  mosaic_image = createPhotomosaic(target_image, input_images, grid_size, reuse_images)

  # write out mosaic
  mosaic_image.save(output_filename, 'PNG')

  print(f"saved output to {output_filename}")
  print('Done.')

if __name__ == '__main__':
  main()