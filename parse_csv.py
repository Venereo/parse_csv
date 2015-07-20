import glob
import csv
import urllib
import urlparse
import itertools


def parse_url(url):
    parts = list(urlparse.urlparse(url))
    parts[2] = urllib.quote(parts[2])
    return urlparse.urlunparse(parts)


for product_info in glob.glob("*product_info.csv"):
    product_image = '_'.join(product_info.split('_')[0:2]) + '_product_image.csv'
    with open(product_info, 'rb') as csvfile_info:
        product_info_reader = csv.reader(csvfile_info, delimiter=',')
        with open(product_image, 'rb') as csvfile_images:
            product_image_reader = csv.reader(csvfile_images, delimiter=',')
            with open('_'.join(product_info.split('_')[0:2]) + '_FINAL.csv', 'wb') as csvfile_output:
                writer = csv.writer(csvfile_output, delimiter=';')
                with open('_'.join(product_info.split('_')[0:2]) + '_COMBINATIONS.csv',
                          'wb') as csvfile_output_combinations:
                    writer_combinations = csv.writer(csvfile_output_combinations, delimiter=';')
                    fieldnames = product_info_reader.next()
                    fieldnames.pop()
                    fieldnames.append('Images URL')
                    fieldnames.append('Web Only')
                    product_image_reader.next()
                    writer.writerow(fieldnames)
                    fieldnames = ['Product ID', 'Attribute (Name:Type:Position)', 'Value (Value:Position)']
                    writer_combinations.writerow(fieldnames)
                    for row_info in product_info_reader:
                        control_combinations = []
                        control_list = []
                        list_all_combinations = row_info[-1].split('\n')[:-1] if len(
                            row_info[-1].split('\n')) > 0 else []
                        for combination in list_all_combinations:
                            control_combinations.append(combination.split(':')[0])
                            temp_combinations = combination.split(':')[1]
                            control_list.append(temp_combinations.split(';')[:-1])
                        for set_ in list(itertools.product(*control_list)):
                            row_combinations = [row_info[0]]
                            temp_line = []
                            for key, combinations in enumerate(control_combinations):
                                if combinations == "Size":
                                    temp_line.append('Tamanho:select:' + str(key))
                                elif combinations == "Color":
                                    temp_line.append('Cor:color:' + str(key))
                                elif combinations == "Size(US)":
                                    temp_line.append('Tamanho:select:' + str(key))
                            row_combinations.append(';'.join(temp_line))
                            temp_line = []
                            for key, subset in enumerate(set_):
                                temp_line.append(subset.strip() + ':' + str(key))
                            row_combinations.append(','.join(temp_line))
                            row_combinations[0] = row_combinations[0].replace('SKU', '')
                            writer_combinations.writerow(row_combinations)
                        csvfile_images.seek(0)
                        product_image_reader.next()
                        for row_images in product_image_reader:
                            images = [parse_url(row_images[1]) for row_images in product_image_reader if
                                      row_info[0] == row_images[0]]
                        row_info.pop()
                        row_info.append(','.join(images))
                        row_info[0] = row_info[0].replace('SKU', '')
                        row_info[6] = ''
                        row_info.append('1')
                        row_info = [' '.join(item.split()) for item in row_info]
                        writer.writerow(row_info)
