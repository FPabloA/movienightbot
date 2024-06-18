from matplotlib import pyplot as plt
from rembg import remove
from PIL import Image
import numpy as np

labelz = ['test', 'trial', 'practice', 'exercise', 'rehearse']
values = [20,20,20,20,20]

if __name__ == "__main__":
    fig = plt.figure(figsize=(6,6))
    patches, txts = plt.pie(values, labels = labelz, labeldistance=0.8)
    for t in txts:
        t.set_horizontalalignment('center')

    plt.savefig("temp_spinner.png")
    #plt.show()
    
    input_path = 'temp_spinner.png'
    output_path = 'temp_spinner.png'
    print('before rembg')
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)