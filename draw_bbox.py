import cv2
import os
import json

# Set the folder path containing the images
image_folder = './mlb_val_set/'

# Set the output JSON file path
output_file = 'annotations_mlb_val_set.json'

# Define the category
category_1 = {
    "id": 1,
    "name": "lo",
    "supercategory": "lo",
}
category_2 = {
    "id": 2,
    "name": "li",
    "supercategory": "li",
}
category_3 = {
    "id": 3,
    "name": "ri",
    "supercategory": "ri",
}
category_4 = {
    "id": 4,
    "name": "ro",
    "supercategory": "ro",
}

# Initialize the COCO annotation dictionary
coco_annotation = {
    "info": {
        "description": "Object detection annotations in COCO format",
        "version": "1.0",
        "year": 2023,
        "date_created": "2023-06-26"
    },
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": [category_1, category_2, category_3, category_4]
}




# Read images from the folder and draw bounding boxes
image_id = 1
annotation_id = 1
file_list = os.listdir(image_folder)
local_count = len(file_list)
for filename in file_list:
    image_path = os.path.join(image_folder, filename)
    image = cv2.imread(image_path)
    print("file name", filename)
    with open(output_file, 'w') as file:
        json.dump(coco_annotation, file)

    # Get image information
    height, width, _ = image.shape

    # Create image entry in COCO annotation dictionary
    image_entry = {
        "id": image_id,
        "file_name": filename,
        "height": height,
        "width": width
    }
    coco_annotation["images"].append(image_entry)

    window_name = "Image Window"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # Display the image and draw bounding boxes
    cv2.imshow(window_name, image)

    annotations = []

    while True:
        # Get user input for bounding box coordinates
        bbox = cv2.selectROI(window_name, image)
        x, y, w, h = bbox


        while True:
            key = cv2.waitKey(0) & 0xFF
            if key in [ord('1'), ord('2'), ord('3'), ord('4')]:
                label = key - ord('0')  # Convert ASCII to numeric value
                break
            else:
                print("Invalid key. Press 1, 2, 3, or 4 to assign a label.")


        # Create annotation entry in COCO annotation dictionary
        annotation_entry = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": label,
            "bbox": [x, y, w, h],
            "area": w * h,
            "iscrowd": 0
        }
        coco_annotation["annotations"].append(annotation_entry)
        annotation_id += 1


        # Draw the bounding box on the image
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)



        # Display the updated image
        cv2.imshow(window_name, image)

        # Wait for user key press
        key = cv2.waitKey(0)


        if key == ord('c'):
            break


        
    local_count -= 1
    print("Remaining images", local_count)
    if local_count % 10:
        print("saving intermediate results, images saved so far", len(file_list)-local_count)
        with open(output_file, 'w') as file:
            json.dump(coco_annotation, file)


    image_id += 1

# Save the COCO annotations to JSON file
with open(output_file, 'w') as filefinal:
    json.dump(coco_annotation, filefinal)

cv2.destroyAllWindows()
print("Annotations saved to JSON file.")
