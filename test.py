from plaid import Plaid 
import helper

url = 'https://hddesktopwallpapers.in/wp-content/uploads/2015/09/cat-eyes-cute.jpg'
img_path = helper.img_from_url.get(url)
tartan_size = 128
num_of_band = 5
colors = helper.get_img_colors(img_path, num_of_band)
pivots = helper.get_sorted_pivots(5)

def main():
    tartan = Plaid(colors, pivots, tartan_size, 'tartan')
    print(tartan.get_png(1080,1024))
    print(tartan.array)
    tartan.show(1080, 800)
    return
  
if __name__=="__main__":
    main()
