from PIL import Image, ImageChops
import os
def compare_images():
    person_on_cam = Image.open("images/person.jpg")
    for filename in os.listdir("resources"):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_file = os.path.join("resources", filename)
            print(f"Processing file: {image_file}")
            person = Image.open(image_file)
            if person_on_cam.size != person.size:
                continue
            difference = ImageChops.difference(person_on_cam, person)
            if difference.getbbox() is None:
                print("The images are the same")
                return True
            else:
                print("diff:", difference.getbbox())
    print("The images are different")
    return False

# compare_images("images/person.jpg")