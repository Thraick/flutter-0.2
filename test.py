import base64
from PIL import Image
from io import BytesIO
import json
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["tee"], allow_remote=True)
def save_image(base64_string, output_path):

    print(len(base64_string))
    # Add padding if necessary
    missing_padding = len(base64_string) % 4
    if missing_padding != 0:
        base64_string += '=' * (4 - missing_padding)

    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_string)

    # Open the image using PIL
    image = Image.open(BytesIO(image_bytes))

    # Save the image to the output path
    image.save(output_path)

# Example usage
base64_string = ""
with open("./testing_data.json", "r") as image_data:
    data = json.load(image_data)
    base64_string = data["image"][0]
    # base64_string = data["image"]

output_path = "output_image22.jpg"

save_image(base64_string, output_path)
